# Copyright (C) Microsoft Corporation, All rights reserved.

"""
The purpose of this script is to summarize Omega output results for later export.

DEPRECATED: Use create-assertion.py instead.

"""
import argparse
import datetime
import glob
import json
import logging
import os
import subprocess
import sys
import tempfile
import uuid

import requests
from dateutil.parser import parse as date_parse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from packageurl import PackageURL

logging.basicConfig(level=logging.INFO)

class CreateReview:
    package_url = None
    input_path = None
    security_reviews_path = None
    analysis_date = None
    toolshed_version = None
    links = []

    def __init__(self, args): 
        """Creates a new CreateReview object."""
        self.package_url = PackageURL.from_string(args.get('package_url'))
        if not self.package_url:
            raise ValueError("Invalid package URL")

        self.input_path = args.get('input_path')
        if not os.path.isdir(self.input_path):
            raise ValueError("Input path is not a directory")

        self.security_reviews_path = args.get('security_reviews_path')
        if not os.path.isdir(self.security_reviews_path):
            raise ValueError("Security reviews path is not a directory")

    def get_metadata(self):
        """Extracts metadata from the input directory."""
        filenames = glob.glob(self.input_path + '/**/summary-metadata.json', recursive=True)
        if len(filenames) == 1:
            with open(filenames[0], 'r') as f:
                data = json.load(f)
                self.analysis_date = date_parse(data.get('analysis_date', datetime.datetime.now().isoformat()))
                self.toolshed_version = data.get('toolshed_version')
        else:
            logging.warning(f"Found {len(filenames)} summary-metadata.json files. Expected 1.")
            return

    def get_urls(self, deps_metadata: dict) -> list:
        """Extracts URLs from a given set of metadata from deps.dev."""
        urls = []
        if not self.package_url:
            return []

        if deps_metadata:
            urls.append({
                'title': 'Home Page',
                'url': deps_metadata.get('version', {}).get('links', {}).get('homepage')
            })
            urls.append({
                'title': 'Project Issue Tracker',
                'url': deps_metadata.get('version', {}).get('links', {}).get('issues')
            })
            urls.append({
                'title': 'Project Repository',
                'url': deps_metadata.get('version', {}).get('links', {}).get('repo')
            })

        if self.package_url.namespace:
            res = f'https://deps.dev/{self.package_url.type}/{self.package_url.namespace}/{self.package_url.name}'
        else:
            res = f'https://deps.dev/{self.package_url.type}/{self.package_url.name}'

        if self.package_url.version:
            res += '/' + self.package_url.version
        urls.append({
            'title': 'Package on deps.dev',
            'url': res
        })

        # Ensure all URLs are valid
        urls = filter(lambda u: u['url'].startswith('http'), urls)
        return urls

    def check_toolshed(self):
        """Checks if the package is clean in Toolshed."""
        logging.info('Checking Toolshed results for findings...')
        codeql_files = glob.glob(self.input_path.rstrip('/') + "/**/tool-codeql-*.sarif", recursive=True)
        for codeql_file in codeql_files:
            with open(codeql_file, 'r') as f:
                data = json.load(f)
                for run in data['runs']:
                    if len(run.get('results', [])) > 0:
                        return False
        
        # Other tool findings to automatically fail on
        fail_on_findings = ['[detect-secrets]', '[nodejsscan]', '[semgrep]']
        summary_console_files = glob.glob(self.input_path.rstrip('/') + "/**/summary-console.txt", recursive=True)
        for summary in summary_console_files:
            with open(summary, 'r') as f:
                summary_text = f.read()
                if any([f in summary_text for f in fail_on_findings]):
                    return False
        return True

    def check_reproducible(self):
        """Checks if the package is reproducible (via oss-reproducible)."""
        logging.info('Checking for reproducibility using oss-reproducible...')
        result = False
        output_filename =  os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + ".json")
        try:
            res = subprocess.run(['oss-reproducible', '-o', output_filename, self.package_url.to_string()], timeout=900)
            if res.returncode == 0:
                with open(output_filename, 'r') as f:
                    data = json.load(f)
                    if len(data) > 0 and data[0].get('IsReproducible') == True:
                        result = True
        except Exception as msg:
            logging.warning('Error running oss-reproducible: %s', msg, exc_info=True)
        
        try:
            os.remove(output_filename)
        except:
            pass

        return result

    def check_scorecard(self):
        """Checks the package's scorecard data.
        
        NOT CURRENTLY USED.
        """
        try:
            if self.package_url.type == 'npm':
                if self.package_url.namespace:
                    target = 'npm=' + self.package_url.namespace + '/' + self.package_url.name
                else:
                    target = 'npm=' + self.package_url.name
            else:
                logging.warning('Unsupported package type: %s', self.package_url.type)
                return

            GITHUB_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')
            if not GITHUB_TOKEN:
                logging.warning('GitHub access token not set.')
                return

            res = subprocess.run(['docker', 'run', '-e', f'GITHUB_AUTH_TOKEN={GITHUB_TOKEN}',
                                  'gcr.io/openssf/scorecard:stable', '--format=json',
                                  f'--{target}'], timeout=900, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode == 0:
                data = json.loads(res.stdout.decode('utf-8'))
                for check in data.get('checks', []):
                    if check.get('name') == 'Dangerous-Workflow' and check.get('score', 0) < 10:
                        return False
                    if check.get('name') == 'Vulnerabilities' and check.get('score', 0) < 10:
                        return False
        except Exception as msg:
            logging.warning('Error running scorecard check: %s', msg, exc_info=True)
        return True
        
    def check_public_vulnerabilities(self):
        # Check for public advisories
        logging.info('Checking deps.dev for public vulnerabilities...')
        if self.package_url.namespace:
            res = requests.get(f'https://deps.dev/_/s/{self.package_url.type}/p/{self.package_url.namespace}/{self.package_url.name}/v/{self.package_url.version}')
        else:
            res = requests.get(f'https://deps.dev/_/s/{self.package_url.type}/p/{self.package_url.name}/v/{self.package_url.version}')
        
        if res.status_code == 200:
            deps_metadata = res.json()
            self.links = self.get_urls(deps_metadata)
            if deps_metadata.get('version', {}).get('advisories', []):
                logging.info('Found public advisories, will not create review.')
                return False
        else:
            return False
        return True

    def create_review(self):
        logging.info('Creating review...')
        env = Environment(loader=FileSystemLoader('etc'), autoescape=select_autoescape())
        template = env.get_template('security-review.template')
        result = template.render({
            'package_urls': [self.package_url],
            'analysis_date': self.analysis_date,
            'analysis_version': self.toolshed_version,
            'links': self.links,
        })
        
        if self.package_url.namespace:
            output_file = os.path.join(self.security_reviews_path, self.package_url.type, self.package_url.namespace, self.package_url.name, f'omega-review-{self.analysis_date.strftime("%Y-%m-%d")}.md')
        else:
            output_file = os.path.join(self.security_reviews_path, self.package_url.type, self.package_url.name, f'omega-review-{self.package_url.version}-{self.analysis_date.strftime("%Y-%m-%d")}.md')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        logging.info('Complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--package-url', required=True, help='Package URL to analyze', type=str)
    parser.add_argument('-i', '--input-path', required=True, help='Toolshed output path', type=str)
    parser.add_argument('-r', '--security-reviews-path', required=True, help='Security review output path', type=str)
    args = parser.parse_args()
    
    logging.info('Processing: %s', args.input_path)
    try:
        review = CreateReview(vars(args))
        review.get_metadata()

        if not review.check_toolshed():
            logging.warning('Toolshed output is not clean. Review will not be created.')
        elif not review.check_public_vulnerabilities():
            logging.warning('Package has public advisories. Review will not be created.')
        elif not review.check_reproducible():
            logging.warning('Package is not reproducible. Review will not be created.')
        else:
            # Only create a review if everything else is clean.
            review.create_review()
    except Exception as msg:
        logging.error("Error creating review: %s", msg, exc_info=True)
        sys.exit(1)
        