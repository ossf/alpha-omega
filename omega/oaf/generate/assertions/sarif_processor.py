import json


class SarifProcessor:
    def __init__(self, sarif):
        if isinstance(sarif, dict):
            self.sarif = sarif
        elif isinstance(sarif, str):
            self.sarif = json.loads(sarif)
        else:
            raise ValueError("SarifProcessor must be initialized with a dict or string")

    @property
    def findings(self):
        rules_map = {}
        for run in self.sarif.get("runs", []):
            for rule in run.get("tool", {}).get("driver", {}).get("rules", []):
                rules_map[rule.get("id")] = {
                    "name": rule.get("name"),
                    "short_description": rule.get("shortDescription", {}).get("text"),
                    "full_description": rule.get("fullDescription", {}).get("text"),
                }
                for property in rule.get("properties", {}):
                    rules_map[rule.get("id")][property] = rule.get(
                        "properties", {}
                    ).get(property)

        for run in self.sarif.get("runs", []):
            for result in run.get("results", []):
                rule = rules_map.get(result.get("ruleId"))
                if not rule:
                    continue

                for location in result.get("locations", []):
                    physical_location = location.get("physicalLocation", {})
                    _filename = physical_location.get("artifactLocation", {}).get("uri")
                    if _filename is None:
                        _filename = physical_location.get("address", {}).get(
                            "fullyQualifiedName"
                        )

                    snippet = (
                        physical_location.get("contextRegion", {})
                        .get("snippet", {})
                        .get("text")
                    )
                    if snippet is None:
                        snippet = (
                            physical_location.get("region", {})
                            .get("snippet", {})
                            .get("text")
                        )

                    start_line = (
                        physical_location.get("region", {}).get("startLine") or 0
                    )
                    end_line = physical_location.get("region", {}).get("endLine") or 5

                    result = {
                        "rule_id": result.get("ruleId"),
                        "filename": _filename,
                        "snippet": snippet,
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                    for property in rule:
                        result[f"rule_{property}"] = rule[property]
                    yield result
