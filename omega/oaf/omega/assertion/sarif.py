"""
Helper class for interacting with SARIF files.
"""
import json
import typing

from .utils import get_complex


class SarifHelper:
    """Helper class for interacting with SARIF files."""
    def __init__(self, sarif: dict | str):
        if isinstance(sarif, dict):
            self.sarif = sarif
        elif isinstance(sarif, str):
            try:
                self.sarif = json.loads(sarif)
                if (
                    self.sarif.get("schema_uri")
                    != "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json"
                ):
                    raise ValueError("Only SARIF v2.1.0 is supported.")

            except json.JSONDecodeError as msg:
                raise ValueError(
                    "Invalid JSON provided, unable to instantiate SarifHelper"
                ) from msg
        else:
            raise ValueError("SarifHelper must be initialized with a dict or string")

    def filter_by_severity(self, min_severity):
        def _filter(result):
            return result.get("rule_defaultConfiguration_level") == min_severity

        return self.filter(_filter)

    def filter(
        self, delegate: typing.Optional[typing.Callable]
    ) -> typing.Generator[dict, None, None]:
        """
        Filters the SARIF results, returning only those that pass a delegate function"""

        rules_map = {}
        for run in self.sarif.get("runs", []):
            for rule in get_complex(run, "tool.driver.rules"):
                rules_map[rule.get("id")] = {
                    "name": rule.get("name"),
                    "short_description": get_complex(rule, "shortDescription.text"),
                    "full_description": get_complex(rule, "fullDescription.text"),
                }
                for _property in rule.get("properties", {}):
                    rules_map[rule.get("id")][_property] = rule.get("properties", {}).get(_property)

        for run in self.sarif.get("runs", []):
            tool_name = ":".join(
                get_complex(run, 'driver.organization'),
                get_complex(run, 'driver.name')
            ) + '@' + get_complex(run, 'driver.semanticVersion')
            
            for result in run.get("results", []):
                rule = rules_map.get(result.get("ruleId"))
                if not rule:
                    continue

                for location in result.get("locations", []):
                    physical_location = location.get("physicalLocation", {})
                    _filename = get_complex(
                        physical_location, "artifactLocation.uri"
                    ) or get_complex(physical_location, "address.fullyQualifiedName")

                    snippet = get_complex(
                        physical_location, "contextRegion.snippet.text"
                    ) or get_complex(physical_location, "region.snippet.text")

                    start_line = get_complex(physical_location, "region.startLine") or 0
                    end_line = get_complex(physical_location, "region.endLine") or 5

                    result = {
                        "rule_id": result.get("ruleId"),
                        "filename": _filename,
                        "snippet": snippet,
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                    for _property in rule:
                        result[f"rule_{_property}"] = rule[_property]

                    if not delegate or delegate(result):
                        yield result
