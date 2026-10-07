from typing import Any, List
import ifcopenshell.util.element
from ifc_checker.core.interfaces import IRule
from ifc_checker.core.models import Issue, Severity


class PropertyExistsRule(IRule):
    def __init__(
        self,
        rule_id: str,
        element_type: str,
        property_set_name: str,
        property_name: str,
        severity: Severity = Severity.ERROR,
    ) -> None:
        self._rule_id = rule_id
        self._element_type = element_type
        self._property_set_name = property_set_name
        self._property_name = property_name
        self._severity = severity

    @property
    def rule_id(self) -> str:
        return self._rule_id

    @property
    def description(self) -> str:
        return f"Ensures {self._element_type} has property '{self._property_name}' in '{self._property_set_name}'."

    def execute(self, model: Any) -> List[Issue]:
        issues: List[Issue] = []
        target_elements = model.by_type(self._element_type)

        for element in target_elements:
            if not self._has_property(element):
                issues.append(self._create_issue(element))

        return issues

    def _has_property(self, element: Any) -> bool:
        property_sets = ifcopenshell.util.element.get_psets(element)
        target_pset = property_sets.get(self._property_set_name)

        if not target_pset:
            return False

        property_value = target_pset.get(self._property_name)
        return property_value is not None

    def _create_issue(self, element: Any) -> Issue:
        return Issue(
            rule_id=self.rule_id,
            element_id=getattr(element, "GlobalId", "UNKNOWN_ID"),
            element_type=element.is_a(),
            message=f"Missing property '{self._property_name}' in PSet '{self._property_set_name}'",
            severity=self._severity,
        )
