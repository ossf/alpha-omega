#!/usr/bin/python

import sys
import argparse
import glob
import subprocess
import os
from typing import List
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

class SARIFNormalizer:
    def __init__(self, sarif_directory: str, source_directory: str):
        if not os.path.isdir(sarif_directory):
            raise ValueError(f"{sarif_directory} does not exist.")
        
        if not os.path.isdir(source_directory):
            raise ValueError(f"{source_directory} does not exist.")

        self.sarif_directory = os.path.abspath(sarif_directory)
        self.source_directory = os.path.abspath(source_directory)
        self.source_files = set()

    def find_closest_file(self, filename: str):
        logging.debug(f"Searching for {filename} in a list of length {len(self.source_files)}")
        
        # Algorithm:
        """
        Repeatedly cut off the top-most path section (/foo/bar/quux, bar/quux, quux) until there's
        a candidate that ends with that.
        """
        if not self.source_files:
            return None

        partial = filename
        
        while True:
            if not partial:
                break

            for candidate_file in self.source_files:
                if candidate_file.endswith(partial):
                    if not os.path.isfile(candidate_file):
                        continue
                    return candidate_file
            parts = list(filter(lambda s: s != '', os.path.normpath(partial).split(os.sep)))
            if len(parts) > 1:
                partial = os.path.join(*parts[1:])
            else:
                break   # No more to go
        return None

    def clean_uri(self, uri, marker='/reference-binaries/'):
        """
        Removes everything from uri before (and including) the marker.
        Returns the full uri if the marker isn't found.
        """
        logging.debug("clean_uri(%s)", uri)
        if not uri:
            return uri
        
        return self.find_closest_file(uri)

        #idx = uri.find(marker)
        #if idx != -1:
        #    return uri[(idx + len(marker)):]
        #else:
        #    return uri

    def extract_source_code(self):
        # Extract all content in reference-binaries
        for _filename in glob.glob("*", root_dir=self.source_directory, recursive=False):
            filename = os.path.join(self.source_directory, _filename)
            
            if not os.path.isfile(filename):
                continue

            if filename.endswith('.extracted'):
                continue

            logging.info(f"Extracting source code from {filename}...")

            canary_file = f'{filename}.extracted'
            if not os.path.isfile(canary_file):
                output = subprocess.check_output(["RecursiveExtractor", "-i", filename, "-o", os.path.join(self.source_directory, "src")])
                with open(canary_file, 'w') as f:
                    f.write('');
            else:
                logging.debug("Extraction already completed.")

            # Cache all filenames
            for root, _, files in os.walk(os.path.join(self.source_directory, "src")):
                for name in files:
                    filename = os.path.abspath(os.path.join(root, name))
                    if os.path.isfile(filename):
                        self.source_files.add(filename)

    def modify_sarif_files(self):
        for _filename in glob.glob("*.sarif", root_dir=self.sarif_directory, recursive=False):
            filename = os.path.join(self.sarif_directory, _filename)
            logging.debug(f"Processing {filename}")

            # Load the SARIF file as JSON
            with open(os.path.join(self.sarif_directory, filename), 'r', encoding='utf-8') as f:
                js = json.load(f)

            for run in js.get('runs', []):
                # Replace the originalUriBaseIds field
                if 'originalUriBaseIds' not in run:
                    run['originalUriBaseIds'] = { "SRCROOT": { "uri": "reference-binaries" } }
                else:
                    run['originalUriBaseIds']['SRCROOT'] = { "uri": "reference-binaries" }

                # Replace the artifact locations with a more relative path
                for result in run.get('results', []):
                    for location in result.get('locations', []):
                        uri = location.get('physicalLocation', {}).get('artifactLocation', {}).get('uri')
                        if uri:
                            uri = self.clean_uri(uri)
                            location['physicalLocation']['artifactLocation']['uri'] = uri
                            continue

                        uri = location.get('physicalLocation', {}).get('address', {}).get('fullyQualifiedName')
                        if uri:
                            uri = self.clean_uri(uri)
                            location['physicalLocation']['address']['fullyQualifiedName'] = uri
                            continue

            with open(os.path.join(self.sarif_directory, filename), 'w', encoding='utf-8') as f:
                logging.info(f"Updating {filename}...")
                json.dump(js, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sarif-dir', help="Directory with SARIF files to modify.", type=str, required=True)
    parser.add_argument('--source-dir', help="Directory with source files (or archives) to modify (default: 'reference-binaries' in --sarif-dir)", type=str, required=False)
    args = parser.parse_args()

    logging.info("SARIF Normalizer starting...")
    normalizer = SARIFNormalizer(args.sarif_dir, args.source_dir or os.path.join(args.sarif_dir, 'reference-binaries'))
    normalizer.extract_source_code()
    normalizer.modify_sarif_files()
    logging.info("SARIF Normalizer complete.")

