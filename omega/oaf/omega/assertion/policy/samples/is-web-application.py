import sys
import json

stream = sys.stdin.read()
assertions = json.loads(stream)
for assertion in assertions:
    if assertion.get('predicateType') == "https://github.com/ossf/alpha-omega/characteristic/0.1.0":
        chars = assertion.get('predicate', {}).get('content', {}).get('characteristics', [])
        print('web.application' in chars)
        sys.exit(0)

print("not applicable")
sys.exit(1)
