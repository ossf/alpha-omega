#!/usr/bin/python
# Copyright (C) Microsoft Corporation, All rights reserved.

import base64
import datetime
import os
import json
import re
import hashlib
import ipaddress
import sys
import fnmatch
import socket
from toolshed_sarif import ToolshedSarif
import logging
import traceback

logger = logging.getLogger(__name__)

class PostProcessor:
    toolshed_sarif = None
    purl = None
    findings = []
    summary = {}
    result_set = set()
    short_findings = {}

    cache = {}

    def __init__(self, purl):
        logger.debug('Initializing PostProcessor')
        self.purl = purl
        self.add_summary('purl', self.purl)
        self.toolshed_sarif = ToolshedSarif()

    def process_directory(self, directory):
        for (root, _, filenames) in os.walk(directory):
            for filename in filenames:
                self.process(os.path.join(root, filename))

    def process(self, filename):
        """
        Process an individual file with the appropriate processor.
        """
        func_name = os.path.basename(filename)
        if func_name.startswith('tool-'):
            func_name = func_name.replace('tool-', '')
            func_name = func_name.split('.')[0]
            func_name = func_name.replace('-', '_').strip().lower()
            func_name = f'process_{func_name}'

            # Ignore certain files
            if func_name in ['process_codeql_db_basic', 'process_codeql_db_installed', 'process_codeql_db_installed_codeflow',
                             'process_codeql_db_installed_codeflow_sinks', 'process_strings', 'process_binwalk', 'process_radare2_rabin2']:
                return

            if hasattr(self.__class__, func_name) and callable(getattr(self.__class__, func_name)):
                func = getattr(self.__class__, func_name)
                try:
                    func(self, filename)
                except Exception as msg:
                    print(f"Error running {func_name}: {msg}")
                    traceback.print_exc(file=sys.stdout)
            else:
                print(f"Can't find a function for {func_name}")

    def add_finding(self, check_name, message, filename, content):
        cache_key = f'{check_name}__{message}__{filename}'
        if 'findings' not in self.cache:
            self.cache['findings'] = set()

        if cache_key not in self.cache['findings']:
            self.findings.append({
                'check_name': check_name,
                'message': message,
                'filename': filename,
                'content': content
            })
            self.cache['findings'].add(cache_key)


    def add_result(self, **kwargs):
        """
        Adds a result, via the ToolshedSarif object.
        """
        key = hashlib.sha256(json.dumps(kwargs).encode('utf-8')).hexdigest()
        if key not in self.result_set:
            self.result_set.add(key)
            self.add_finding(kwargs.get('tool_name'), kwargs.get('message'), kwargs.get('filename'), kwargs.get('snippet'))
            return self.toolshed_sarif.add_result(**kwargs)

    def add_error_result(self, tool_name, content):
        """
        Adds an error result, meaning a tool that was unable to complete successfully.
        """
        return self.add_result(**{
            'tool_name': tool_name,
            'level': 'warning',
            'message': f"An error occurred when processing [{tool_name}]",
            'filename': self.purl,
            'start_line': 1,
            'snippet': content,
            'end_line': len(content.splitlines()),
            'rule_id': f'{tool_name}/analysis-error',
            'rule_name': 'Error analyzing target',
            'rule_short_description': 'An error was encountered when [{0}] was attempting to analyze the component.'.format(tool_name),
            'purl': self.purl
        })

    def add_summary(self, key, content):
        """
        Shortcut function add summary content, if it exists.
        """
        if content:
            self.summary[key] = content

    def strip_ossgadget_banner(self, text: str) -> str:
        """
        Removes the OSS Gadget banner from a string.
        """
        if not text:
            return text
        banner_regex = re.compile(r'^[\s_/\\\|,\)\(`]+OSS Gadget - oss-.* [0-9\.]+\+[0-9a-f]* - github\.com/Microsoft/OSSGadget\n*')
        text = banner_regex.sub('', text)
        return text

    def process_oss_find_source(self, filename):
        """
        Processes results created by OSS Find Source.
        """
        with open(filename) as f:
            content = self.strip_ossgadget_banner(f.read()).strip()

        if not content:
            return

        if filename.endswith('.stderr'):
            self.add_error_result('oss-find-source', content)
            return

        if filename.endswith('.sarif'):
            source = []
            js = json.loads(content)
            for run in js.get('runs', []):
                for result in run.get('results', []):
                    source_repo = result.get('message', {}).get('text')
                    likelihood = result.get('rank')
                    for location in result.get('locations', []):
                        package_url = location.get('physicalLocation', {}).get('address', {}).get('name')
                        if source_repo and package_url:
                            source.append({
                                'likelihood': likelihood,
                                'source_repository': source_repo,
                                'package_url': package_url
                            })
            if source:
                self.add_summary('source-repository', source)

    def process_application_inspector(self, filename):
        """
        Processes results created by Application Inspector.
        """
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            self.add_error_result('application-inspector', content)

        if filename.endswith('.json'):
            js = json.loads(content)
            self.add_summary('description', js.get('metaData', {}).get('description'))
            self.add_summary('tags', js.get('metaData', {}).get('uniqueTags'))
            self.add_summary('file_extensions', js.get('metaData', {}).get('fileExtensions'))
            languages = js.get('metaData', {}).get('languages', {})
            languages = list(languages.keys()) if languages else []
            self.add_summary('languages', languages)

    def process_bandit(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            pass   # Uninteresting

        if filename.endswith('.json'):
            js = json.loads(content)
            for result in js.get('results', []):
                if result.get('issue_severity') == "LOW" or result.get('issue_confidence') == "LOW":
                    continue    # Filter low-quality

                snippet = []
                for line in result.get('code').splitlines():
                    matches = re.match(r'^\d+\s+(.*)', line)
                    if matches:
                        snippet.append(matches.group(1).strip())

                self.add_result(**{
                    'tool_name': 'bandit',
                    'level': 'warning',
                    'message': result.get('issue_text'),
                    'filename': result.get('filename'),
                    'start_line': result.get('line_number'),
                    'snippet': '\n'.join(snippet),
                    'end_line': result.get('line_number') + len(snippet),
                    'rule_id': 'bandit/{0}'.format(result.get('test_name')),
                    'rule_short_description': result.get('issue_text'),
                    'purl': self.purl
                })

    def process_checksec(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            self.add_error_result('checksec', content)

        if filename.endswith('.json'):
            content = re.sub(r',\s*\]', ']', content)
            content = re.sub(r',\s*\}', '}', content)
            js = json.loads(content)

            for _filename, value in js.items():
                if _filename == "dir":
                    continue

                # What do we care about logging?
                if (value.get('relro') == "none" or
                        value.get('canary') == "no" or
                        value.get('nx') == "no" or
                        value.get("pie") == "no" or
                        value.get("rpath") == "yes" or
                        value.get("fortify_source") == "no"):

                    snippet = json.dumps({_filename: value}, indent=2)
                    self.add_result(**{
                        'tool_name': 'checksec',
                        'level': 'warning',
                        'message': "Checksec warning",
                        'filename': _filename,
                        'start_line': 1,
                        'snippet': snippet,
                        'end_line': len(snippet.splitlines()) + 1,
                        'rule_id': 'checksec/warning',
                        'rule_short_description': 'An important binary mitigation was not detected.',
                        'purl': self.purl
                    })

    def process_clamscan(self, filename):
        with open(filename) as f:
            content = f.read()

        lines = content.splitlines()
        if filename.endswith('.error') and content:
            if (len(lines) == 4 and
                    lines[1].strip().startswith('LibClamAV Warning: ***  The virus database is older than')):
                # This is OK, we periodically refresh ClamAV, but we don't need it to be completely up to date.
                return
            self.add_error_result('clamav', content)
            return

        if filename.endswith('.txt') and 'Infected files: 0' not in content:
            lines_findings = list(filter(lambda l: l.startswith('/') and not l.endswith('OK') and not l.endswith('Empty file') and l.strip(), lines))
            lines_pua = list(filter(lambda l: 'PUA' in l, lines_findings))
            lines_mal = list(filter(lambda l: 'PUA' not in l, lines_findings))

            if lines_pua:
                self.add_result(**{
                    'tool_name': 'clamav',
                    'level': 'error',
                    'message': "ClamAV alert (PUA) - (high false positives)",
                    'filename': self.purl,
                    'start_line': 1,
                    'snippet': '\n'.join(lines_pua),
                    'end_line': len(lines_pua) + 1,
                    'rule_id': 'clamav/pua',
                    'rule_short_description': 'ClamAV identified a potentially unwanted application (PUA).',
                    'purl': self.purl
                })

            if lines_mal:
                self.add_result(**{
                    'tool_name': 'clamav',
                    'level': 'error',
                    'message': "ClamAV alert (Malware)",
                    'filename': self.purl,
                    'start_line': 1,
                    'snippet': '\n'.join(lines_mal),
                    'end_line': len(lines_mal) + 1,
                    'rule_id': 'clamav/malware',
                    'rule_short_description': 'ClamAV identified potentially malicious content.',
                    'purl': self.purl
                })

    def process_codeql_basic(self, filename):
        self.process_sarif_generic(filename, 'codeql_basic')

    def process_codeql_installed(self, filename):
        self.process_sarif_generic(filename, 'codeql_installed')

    def process_sarif_generic(self, filename, processor_name, filter_rules=True, ignore_error=False):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            if not ignore_error and 'codeql' in filename and 'Interpreting results.' not in content:
                self.add_error_result(processor_name, content)
            elif not ignore_error and 'codeql' not in filename and content:
                self.add_error_result(processor_name, content)
            return

        if filename.endswith('.sarif'):
            js = json.loads(content)

            target_rules = {}

            for run in js.get('runs', []):
                for rule in run.get('tool', {}).get('driver', {}).get('rules', []):
                    if filter_rules:
                        tags = list(map(str.lower, rule.get('properties', {}).get('tags', [])))
                        if 'security' in rule.get('id').lower() or any(['security' in t or 'cwe' in t or 'owasp' in t for t in tags]):
                            target_rules[rule.get('id')] = rule
                    else:
                        target_rules[rule.get('id')] = rule

            for run in js.get('runs', []):
                for result in run.get('results', []):
                    rule_id = result.get('ruleId')
                    if rule_id not in target_rules:
                        continue

                    rule_name = target_rules[rule_id].get('name', rule_id)
                    rule_short_description = target_rules[rule_id].get('shortDescription', {}).get('text')
                    if not rule_short_description:
                        target_rules[rule_id].get('fullDescription', {}).get('text')
                    if not rule_short_description:
                        rule_short_description = rule_name

                    for location in result.get('locations', []):
                        physical_location = location.get('physicalLocation', {})
                        _filename = physical_location.get('artifactLocation', {}).get('uri')
                        if _filename is None:
                            _filename = physical_location.get('address', {}).get('fullyQualifiedName')

                        snippet = physical_location.get('contextRegion', {}).get('snippet', {}).get('text')
                        if snippet is None:
                            snippet = physical_location.get('region', {}).get('snippet', {}).get('text')

                        start_line = physical_location.get('region', {}).get('startLine') or 0
                        end_line = physical_location.get('region', {}).get('endLine') or 5

                        self.add_result(**{
                            'tool_name': processor_name,
                            'level': 'error',
                            'message': result.get('message', {}).get("text"),
                            'filename': _filename,
                            'start_line': start_line,
                            'snippet': snippet,
                            'end_line': end_line,
                            'rule_id': f'{processor_name}/{rule_id}',
                            'rule_name': rule_name,
                            'rule_short_description': rule_short_description,
                            'purl': self.purl
                        })

    def process_npm_audit(self, filename):
        with open(filename) as f:
            content = f.read()

        if filename.endswith('.error') and content:
            self.add_error_result('npm-audit', content)
            return

        if filename.endswith('.json'):
            js = json.loads(content)
            for _, advisory in js.get('advisories', {}).items():
                for finding in advisory.get('findings', []):
                    snippet = json.dumps(finding, indent=2)
                    self.add_result(**{
                        'tool_name': 'npm-audit',
                        'level': 'warning',
                        'message': "{0} (CVEs: {1})".format(advisory["title"], ", ".join(advisory["cves"]) or "(None)"),
                        'filename': self.purl,
                        'start_line': 1,
                        'snippet': snippet,
                        'end_line': len(snippet.splitlines()) + 1,
                        'rule_id': 'npm-audit/{0}'.format(advisory["title"]),
                        'rule_short_description': str(advisory["overview"]).strip(),
                        'purl': self.purl
                    })


    def process_shhgit(self, filename):
        with open(filename) as f:
            content = f.read()

        if filename.endswith('.error') and content:
            self.add_error_result('shhgit', content)
            return

        lines = content.splitlines()
        if filename.endswith('.csv') and len(lines) > 1:
            for line in lines[1:]:
                if not line:
                    continue
                snippet = "{0}\n{1}".format(lines[0], line)
                self.add_result(**{
                    'tool_name': 'shhgit',
                    'level': 'warning',
                    'message': "A secret was found.",
                    'filename': self.purl,
                    'start_line': 1,
                    'snippet': snippet,
                    'end_line': 3,
                    'rule_id': 'shhgit/secret',
                    'rule_short_description': "A secret was found.",
                    'purl': self.purl
                })

    def process_secretscanner(self, filename):
        if not filename.endswith('.json'):
            return

        with open(filename) as f:
            content = json.load(f)
            if not content:
                return

        for secret in (content.get('Secrets', []) or []):
            rule_name_slug = self.slug(secret.get('Matched Rule Name'))
            if secret.get('Matched Part') in ['filename', 'path']:
                snippet = secret.get('Full File Name', '')
            else:
                snippet = secret.get('Matched File Contents', '')

            self.add_result(**{
                'tool_name': 'secretscanner',
                'level': 'warning',
                'message': "A secret was found.",
                'filename': secret.get('Full File Name', self.purl),
                'start_line': 1,
                'snippet': snippet,
                'end_line': 3,
                'rule_id': f"secretscanner/{rule_name_slug}",
                'rule_short_description': secret.get('Matched Rule Name'),
                'purl': self.purl
            })


    def process_application_inspector_diff(self, filename):
        with open(filename) as f:
            content = f.read()

        if not filename.endswith('.json'):
            return

        js = json.loads(content)
        tags = list(map(lambda s: s.get('tag'), js.get('tagDiffList', [])))
        if tags:
            self.add_result(**{
                'tool_name': 'application-inspector-diff',
                'level': 'warning',
                'message': "New characteristics were found.",
                'filename': self.purl,
                'start_line': 1,
                'snippet': '\n'.join(sorted(tags)),
                'end_line': len(tags),
                'rule_id': 'application-inspector/new-tag',
                'rule_short_description': "A new characteristic was found.",
                'purl': self.purl
            })

    def process_strings_diff(self, filename):
        with open(filename, 'r') as f:
            content = f.read()

        if not content or not content.strip():
            return

        self.add_result(**{
            'tool_name': 'string-diff',
            'level': 'warning',
            'message': "New strings were found since the previous version.",
            'filename': self.purl,
            'start_line': 1,
            'snippet': f'{filename}\n\n{content}',
            'end_line': len(content.splitlines()) + 3,
            'rule_id': 'string-diff/new-string-since-previous',
            'rule_short_description': "A new string was found since the previous version.",
            'purl': self.purl
        })


    def process_detect_secrets(self, filename):
        with open(filename) as f:
            content = f.read()

        if filename.endswith('.error') and content:
            self.add_error_result('detect-secrets', content)
            return

        if filename.endswith('.json'):
            js = json.loads(content)
            for fn, result in js.get('results', {}).items():
                if fn.endswith('package-lock.json') or '/test/' in fn or fn.endswith('.md'):
                    continue
                snippet = json.dumps({fn: result}, indent=2)
                self.add_result(**{
                        'tool_name': 'detect-secrets',
                        'level': 'warning',
                        'message': "A secret was found.",
                        'filename': self.purl,
                        'start_line': 1,
                        'snippet': snippet,
                        'end_line': len(snippet.splitlines()) + 1,
                        'rule_id': 'detect-secrets/secret',
                        'rule_short_description': "A secret was found.",
                        'purl': self.purl
                    })

    def process_devskim(self, filename):
        self.process_sarif_generic(filename, 'devskim', filter_rules=False)

    def process_cppcheck(self, filename):
        with open(filename) as f:
            content = f.read()

        if filename.endswith('.error') and content:
            self.add_error_result('cppcheck', content)
            return

        for line in content.splitlines():
            parts = line.split("~!~")
            if len(parts) != 7:
                continue
            _filename = parts[0]
            line_number = parts[1]
            severity = parts[2]
            message = parts[3]
            snippet = parts[4].strip()
            error_id = parts[5]
            cwe = parts[6]

            if severity not in ['error', 'warning']:
                continue

            self.add_result(**{
                'tool_name': 'cppcheck',
                'level': severity,
                'message': '{0} (CWE: {1}'.format(message, cwe or "(None)"),
                'filename': _filename,
                'start_line': line_number,
                'snippet': snippet,
                'end_line': line_number + 1,
                'rule_id': f'cppcheck/{error_id}',
                'rule_short_description': f'CppCheck: {error_id}',
                'purl': self.purl
            })

    def slug(self, s):
        try:
            if s:
                return re.sub(r'[\W_]+', '-', s.strip().lower())
        except:
            pass
        return s

    def process_brakeman(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            self.add_error_result('brakeman', content)
            return

        if filename.endswith('.json'):
            js = json.loads(content)
            for key in ['warnings', 'errors']:
                for result in js.get(key, []):
                    if result.get('confidence') not in ['High', 'Medium']:
                        continue
                    line = result.get('line') or 1
                    self.add_result(**{
                        'tool_name': 'brakeman',
                        'level': 'error',
                        'message': result.get('message'),
                        'filename': result.get('file'),
                        'start_line': line,
                        'snippet': result.get('code'),
                        'end_line': line + 1,
                        'rule_id': 'brakeman/{0}'.format(self.slug(result.get('warning_type'))),
                        'rule_short_description': result.get("warning_type"),
                        'purl': self.purl
                    })


    def process_lizard(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            self.add_error_result('lizard', content)
            return

        if filename.endswith('.txt'):
            lines = content.splitlines()
            if lines:
                self.add_result(**{
                    'tool_name': 'lizard',
                    'level': 'warning',
                    'message': 'This package was found to have high code complexity.',
                    'filename': self.purl,
                    'start_line': 1,
                    'snippet': content,
                    'end_line': len(lines) + 1,
                    'rule_id': 'lizard/code-complexity',
                    'rule_short_description': 'This package was found to have high code complexity.',
                    'purl': self.purl
                })

    def process_manalyze(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if not filename.endswith('.json'):
            return

        js = json.loads(content)
        for data in js:
            for _filename, result in data.items():
                for plugin_name, plugin_value in result.get('Plugins', {}).items():
                    snippet = json.dumps(plugin_value.get('plugin_output'), indent=2)
                    self.add_result(**{
                        'tool_name': 'manalyze',
                        'level': 'warning',
                        'message': plugin_value.get('summary'),
                        'filename': _filename,
                        'start_line': 1,
                        'snippet': snippet,
                        'end_line': len(snippet.splitlines()) + 1,
                        'rule_id': 'manalyze/{0}'.format(self.slug(plugin_name)),
                        'rule_short_description': plugin_value.get('summary'),
                        'purl': self.purl
                    })

    def process_nodejsscan(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            self.add_error_result('nodejsscan', content)
            return

        if filename.endswith('.json'):
            js = json.loads(content)
            for _, vulns in js.get('sec_issues').items():
                for vuln in vulns:
                    self.add_result(**{
                        'tool_name': 'nodejsscan',
                        'level': 'warning',
                        'message': vuln.get('description'),
                        'filename': vuln.get('filename'),
                        'start_line': vuln.get('line'),
                        'snippet': vuln.get('lines'),
                        'end_line': vuln.get('line') + len(vuln.get('lines').splitlines()),
                        'rule_id': 'nodejsscan/{0}'.format(vuln.get('tag')),
                        'rule_short_description': vuln.get('title'),
                        'purl': self.purl
                    })

    def process_oss_detect_backdoor(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        #if filename.endswith('.error'):
        #    self.add_error_result('oss-detect-backdoor', content)
        #    return

        if filename.endswith('.json'):
            js = json.loads(content)
            matches = js.get('metaData', {}).get('detailedMatchList', [])
            for match in matches:
                if 'LOLBAS' in match.get('ruleDescription', ''):
                    continue
                self.add_result(**{
                    'tool_name': 'oss-detect-backdoor',
                    'level': 'error',
                    'message': match.get('ruleDescription'),
                    'filename': match.get('fileName', ''),
                    'snippet': match.get('excerpt'),
                    'start_line': int(match.get('startLocationLine', '1')),
                    'end_line': int(match.get('endLocationLine', '1')),
                    'rule_id': match.get('ruleId'),
                    'rule_short_description': match.get('ruleDescription'),
                    'purl': self.purl
                })

    def process_oss_defog(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            self.add_error_result('oss-defog', content)
            return
        if filename.endswith('.txt'):
            findings = []
            line_queue = []
            for line in content.splitlines():
                if line.startswith('/tmp/'):
                    if line_queue:
                        findings.append('\\n'.join(line_queue))
                    line_queue = [line]
                else:
                    line_queue.append(line)
            if line_queue:
                findings.append('\\n'.join(line_queue))

            for finding in findings:
                parts = finding.split(':', 1)
                filename = parts[0].split('/', 3)[-1]
                snippet = parts[1]

                self.add_result(**{
                    'tool_name': 'oss-defog',
                    'level': 'warning',
                    'message': "Obfuscated code found.",
                    'filename': filename,
                    'snippet': snippet,
                    'start_line': 1,
                    'end_line': 2,
                    'rule_id': 'oss-defog/obfuscation',
                    'rule_short_description': "Obfuscated code found.",
                    'purl': self.purl
                })

    def process_oss_detect_cryptography(self, filename):
        with open(filename) as f:
            content = self.strip_ossgadget_banner(f.read()).strip()

        if not content:
            return

        nonblank_lines = len(list(map(lambda s: s, content.splitlines())))

        if filename.endswith('.error'):
            if nonblank_lines > 1:
                self.add_error_result('oss-detect-cryptography', content)
            return

        if filename.endswith('.txt'):
            for line in content.splitlines():
                if '[x]' in line.lower():
                    self.add_result(**{
                        'tool_name': 'oss-detect-cryptography',
                        'level': 'warning',
                        'message': "Cryptographic implementation found",
                        'filename': self.purl,
                        'start_line': 1,
                        'snippet': line.strip(),
                        'end_line': 2,
                        'rule_id': 'oss-detect-cryptography/implementation',
                        'rule_short_description': "Cryptographic implementation found",
                        'purl': self.purl
                    })
                    self.add_summary('implements-cryptography', True)

    def process_semgrep(self, filename):
        self.process_sarif_generic(filename, 'semgrep', filter_rules=True, ignore_error=True)

    def process_strace(self, filename):
        with open(filename) as f:
            content = f.read().strip()

        if not content:
            return

        if 'strace_network' not in self.cache:
            self.cache['strace_network'] = set()

        if 'strace_filename' not in self.cache:
            self.cache['strace_filename'] = {}

        if 'ignore_filenames' not in self.cache:
            ignore_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'etc/strace-ignore.json')
            if os.path.isfile(ignore_file):
                with open(ignore_file, 'r') as f:
                    self.cache['ignore_filenames'] = json.load(f)
            else:
                self.cache['ignore_filenames'] = {'read': {}, 'write': {}}

        if 'ignore_networks' not in self.cache:
            self.cache['ignore_networks'] = set(['8.8.8.8', '75.75.75.75', '168.63.129.16'])

            try:
                for hostname in ['files.pythonhosted.org', 'pypi.org', 'nuget.org', 'registry.npmjs.com', 'registry.npmjs.org',
                                'dc.services.visualstudio.com', 'dc.applicationinsights.azure.com', 'dc.applicationinsights.microsoft.com',
                                'globalcdn.nuget.org']:
                    self.cache['ignore_networks'] |= set(socket.gethostbyname_ex(hostname)[2])
            except Exception:
                pass

        if filename.endswith('.error') or filename.endswith('.log'):
            return

        lines = content.splitlines()
        for line in lines:
            if line.startswith('connect('):
                match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                if match:
                    ip_addr = match.group(1)
                    if ip_addr not in self.cache['ignore_networks'] and not ipaddress.ip_address(ip_addr).is_private:
                        self.cache['strace_network'].add(ip_addr)

                        self.add_result(**{
                            'tool_name': 'strace-network',
                            'level': 'warning',
                            'message': "Network connection to: {0}".format(ip_addr),
                            'filename': self.purl,
                            'start_line': 1,
                            'snippet': content,
                            'end_line': len(content.splitlines()) + 1,
                            'rule_id': 'strace-network/network-connection',
                            'rule_short_description': "Network connection",
                            'purl': self.purl
                        })
            elif line.startswith('openat('):
                match = re.search(r'openat\([^,]+,\s*\"([^\"]+)\"', line)
                if match:
                    target_filename = match.group(1).strip()

                    is_read = any([c in line for c in ['O_RDONLY', 'O_RDWR']])
                    is_write = any([c in line for c in ['O_WRONLY', 'O_RDWR']])
                    is_directory = 'O_DIRECTORY' in line

                    if is_directory:
                        continue   # Uninteresting

                    if is_read and is_write:
                        rw_string = 'read-write'
                    elif is_read:
                        rw_string = 'read-only'
                    elif is_write:
                        rw_string = 'write-only'

                    if self.should_ignore(target_filename, is_read, is_write):
                        continue

                    if target_filename not in self.cache['strace_filename']:
                        self.cache['strace_filename'][target_filename] = {
                            'read-write': False,
                            'read-only': False,
                            'write-only': False
                        }

                    if self.cache['strace_filename'][target_filename][rw_string]:
                        continue   # Already seen
                    else:
                        self.cache['strace_filename'][target_filename][rw_string] = True

                    snippet = list(filter(lambda s: target_filename in s, lines))
                    self.add_result(**{
                            'tool_name': 'strace-file',
                            'level': 'warning',
                            'message': "File access ({0}): {1}".format(rw_string, target_filename),
                            'filename': self.purl,
                            'start_line': 1,
                            'snippet': '\n'.join(snippet),
                            'end_line': len(snippet) + 1,
                            'rule_id': f'strace-file/file-{rw_string}',
                            'rule_short_description': f"File access {rw_string}",
                            'purl': self.purl
                        })

    def process_tbv(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        result = None

        if filename.endswith('.error'):
            if 'FAILED' in content:
                result = 'Build could not be reproduced.'
            elif content:
                result = 'Error checking reproducibility.'
        else:
            nonblank_lines = list(map(lambda s: s, content.splitlines()))
            if 'FAILED' in nonblank_lines[-1]:
                result = 'Build could not be reproduced.'

        if result:
            self.add_result(**{
                'tool_name': 'tbv',
                'level': 'warning',
                'message': result,
                'filename': self.purl,
                'start_line': 1,
                'snippet': content,
                'end_line': len(content.splitlines()) + 1,
                'rule_id': 'tbv/{0}'.format(self.slug(result)),
                'rule_short_description': result,
                'purl': self.purl
            })

    def process_yara(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            pass   # Uninteresting

        if filename.endswith('.txt'):
            self.add_result(**{
                'tool_name': 'yara',
                'level': 'warning',
                'message': 'yara',
                'filename': self.purl,
                'start_line': 0,
                'snippet': content,
                'end_line': len(content.splitlines()),
                'rule_id': 'yara/',
                'rule_short_description': 'yara',
                'purl': self.purl
            })

    def process_scc(self, filename):
        with open(filename) as f:
            content = f.read()

        if not content:
            return

        if filename.endswith('.error'):
            pass   # Uninteresting

        if filename.endswith('.txt'):
            for line in content.splitlines():
                if line.startswith('Total'):
                    parts = line.split()
                    self.summary['codesize.num_files'] = parts[1]
                    self.summary['codesize.loc'] = parts[2]
                    continue
                if line.startswith('Processed'):
                    parts = line.split()
                    self.summary['codesize.bytes'] = parts[1]

    def generate_description_html(self):
        tags = [f"<li>{tag}</li>" for tag in sorted(self.summary.get('tags', []))]
        if not tags:
            tags = ["<li><i>No tags.</i></li>"]
        messages = sorted(set([f"<strong>{finding.get('check_name')}</strong>: {finding.get('message')}" for finding in self.findings]))
        findings = [f"<li>{finding}</li>" for finding in messages]
        if not findings:
            findings = ["<li><i>No tool findings.</i></li>"]

        template = f"""
        <div spellcheck="false">
        <strong>Package URL:</strong> {self.purl}<br/>
        <strong>Size:</strong> {int(self.summary.get('codesize.loc', 0)):,d} lines, {int(self.summary.get('codesize.bytes', 0)):,d} bytes<br/>
        <strong>Tags:</strong><br/>
        <ul>{''.join(tags)}</ul><br/>
        <strong>Finding Summary</strong><br/>
        <ul>{''.join(findings)}</ul>
        </div>"""
        return template

    def should_ignore(self, target_filename: str, is_read: bool, is_write: bool) -> bool:
        if target_filename is None:
            return True

        cache = self.cache['ignore_filenames']
        read_cache = cache.get('read', {})
        write_cache = cache.get('write', {})

        matches = re.match('pkg:([^/]+)/.*', self.purl)
        if matches:
            purl_type = matches.group(1).strip().lower()
        else:
            return False

        ok_to_read = False
        for pattern in read_cache.get('common', []):
            if fnmatch.fnmatch(target_filename, pattern):
                ok_to_read = True
                break

        if not ok_to_read:
            for pattern in read_cache.get(purl_type, []):
                if fnmatch.fnmatch(target_filename, pattern):
                    ok_to_read = True
                    break

        ok_to_write = False
        for pattern in write_cache.get('common', []):
            if fnmatch.fnmatch(target_filename, pattern):
                ok_to_write = True
                break

        if not ok_to_write:
            for pattern in write_cache.get(purl_type, []):
                if fnmatch.fnmatch(target_filename, pattern):
                    ok_to_write = True
                    break

        if is_read:
            return ok_to_read or ok_to_write
        elif is_write:
            return ok_to_write
        else:  # ??
            return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: postprocess.py purl directory")
        sys.exit(1)

    p = PostProcessor(sys.argv[1])

    runtools_path = os.path.join(os.path.dirname(__file__), 'runtools.sh')
    with open(runtools_path, 'r') as f:
        for line in f.readlines():
            if re.match(r'^ANALYZER_VERSION="(.*)"$', line):
                toolshed_version = line.split('"')[1].strip()
                break

    if os.path.isdir(sys.argv[2]):
        p.process_directory(sys.argv[2])
        p.add_summary('analysis_date', datetime.datetime.now().isoformat())
        p.add_summary('toolshed_version', toolshed_version)

        # SARIF, for the work item attachment
        with open('/opt/result/summary-results.sarif', 'w') as f:
            f.write(p.toolshed_sarif.to_json())

        # HTML, for the work item description
        with open('/opt/result/summary-description.html', 'w') as f:
            f.write(p.generate_description_html())

        # Summary JSON (Metadata)
        with open('/opt/result/summary-metadata.json', 'w') as f:
            f.write(json.dumps(p.summary, indent=2))

        # Summary Text, for the console
        with open('/opt/result/summary-console.txt', 'w') as f:
            for finding in p.findings:
                msg = finding.get('message', '').replace('\n', ' ')
                f.write(f"[{finding.get('check_name')}] {msg}\n")

        sys.exit(0)
    else:
        print(f"Usage: postprocess.py purl directory")
        sys.exit(1)