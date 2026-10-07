import json
from pathlib import Path
from typing import List

from ifc_checker.core.interfaces import IRule
from ifc_checker.rules.dynamic_rules import DynamicPropertyRule


class JSONRuleLoader:
    """A rule loader from a JSON configuration file."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def load_rules(self) -> List[IRule]:
        """Parses JSON and returns a list of IRule objects."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Rule file not found: {self.file_path}")
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        rules: List[IRule] = []
        for item in data.get("rules", []):
            rule_type = item.get("type")
            if rule_type == "PropertyCheck":
                rule = DynamicPropertyRule(
                    rule_id=item["rule_id"],
                    description=item["description"],
                    entity_type=item["params"]["entity_type"],
                    pset_name=item["params"]["pset_name"],
                    property_name=item["params"]["property_name"],
                )
                rules.append(rule)
            else:
                print(f"Warning: Unknown rule type '{rule_type}'. Skipping.")

        return rules
