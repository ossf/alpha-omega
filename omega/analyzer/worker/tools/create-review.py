# Copyright (C) Microsoft Corporation, All rights reserved.

"""
The purpose of this script is to summarize Omega output results for later export.
"""

import requests
import argparse
import os
import sys
import glob
import json
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
from dateutil.parser import parse as date_parse
from packageurl import PackageURL

logging.basicConfig(level=logging.INFO)

class CreateReview:
    package_url = None

    def __init__(self, path, output_path): 
        self.path = path
        self.process_metadata()
        if self.package_url is None:
            raise Exception("Unable to identify package url.")
        self.output_path = output_path

    def get_url(self):
        parts = []
        if self.package_url.type == 'npm':
            if self.package_url.namespace:
                res = f'https://deps.dev/npm/{self.package_url.namespace}/{self.package_url.name}'
            else:
                res = f'https://deps.dev/npm/{self.package_url.name}'
        
            if self.package_url.version:
                res += '/' + self.package_url.version
        else:
            res = self.package_url.to_string()

        return res

    def process_metadata(self):
        filenames = glob.glob(self.path + '/**/summary-metadata.json', recursive=True)
        if len(filenames) != 1:
            logging.warning(f"Found {len(filenames)} summary-metadata.json files. Expected 1.")
            return
        else:
            with open(filenames[0], 'r') as f:
                data = json.load(f)
                self.package_url = PackageURL.from_string(data['purl'])
                self.analysis_date = date_parse(data.get('analysis_date', datetime.datetime.now().isoformat()))
                self.toolshed_version = data.get('toolshed_version', 'unknown')

                logging.debug('Found package URL: ' + self.package_url.to_string())
    
    def is_clean(self):
        codeql_files = glob.glob(self.path + "/**/tool-codeql-*.sarif", recursive=True)
        for codeql_file in codeql_files:
            with open(codeql_file, 'r') as f:
                data = json.load(f)
                for run in data['runs']:
                    if len(run.get('results', [])) > 0:
                        return False
        return True

    def create_review(self):
        if not self.is_clean():
            logging.warning('Omega output is not clean. Review will not be created.')
            return

        # Check for public advisories
        logging.info('Checking deps.dev...')
        if self.package_url.namespace:
            res = requests.get(f'https://deps.dev/_/s/{self.package_url.type}/p/{self.package_url.namespace}/{self.package_url.name}/v/{self.package_url.version}')
        else:
            res = requests.get(f'https://deps.dev/_/s/{self.package_url.type}/p/{self.package_url.name}/v/{self.package_url.version}')
        if res.status_code == 200:
            js = res.json()
            if js.get('version', {}).get('advisories', []):
                logging.info('Found public advisories, will not create review.')
                return
            
        logging.info('Creating review...')
        env = Environment(loader=FileSystemLoader('etc'), autoescape=select_autoescape())
        template = env.get_template('security-review.template')
        result = template.render({
            'package_urls': [self.package_url],
            'analysis_date': self.analysis_date,
            'analysis_version': self.toolshed_version,
            'package_url_href': self.get_url(),
        })
        
        if self.package_url.namespace:
            output_file = os.path.join(self.output_path, self.package_url.type, self.package_url.namespace, self.package_url.name, f'omega-review-{self.analysis_date.strftime("%Y-%m-%d")}.md')
        else:
            output_file = os.path.join(self.output_path, self.package_url.type, self.package_url.name, f'omega-review-{self.package_url.version}-{self.analysis_date.strftime("%Y-%m-%d")}.md')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(result)
        logging.info('Complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', help='Toolshed output path', type=str)
    parser.add_argument('-o', '--output_path', help='Review output path', type=str)
    args = parser.parse_args()

    if (args.input_path and os.path.isdir(args.input_path) and 
            args.output_path and os.path.isdir(args.output_path)):
        print('Processing: {}'.format(args.input_path))
        review = CreateReview(args.input_path, args.output_path)
        review.create_review()
    else:
        parser.print_help()
        sys.exit(1)