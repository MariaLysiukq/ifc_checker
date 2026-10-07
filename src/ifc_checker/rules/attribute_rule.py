from typing import Any, List
from ifc_checker.core.interfaces import IRule
from ifc_checker.core.models import Issue, Severity


class AttributeExistsRule(IRule):
    def __init__(
        self,
        rule_id: str,
        element_type: str,
        attribute_name: str,
        severity: Severity = Severity.ERROR,
    ) -> None:
        self._rule_id = rule_id
        self._element_type = element_type
        self._attribute_name = attribute_name
        self._severity = severity

    @property
    def rule_id(self) -> str:
        return self._rule_id

    @property
    def description(self) -> str:
        return f"Ensures all {self._element_type} elements have the '{self._attribute_name}' attribute populated."

    def execute(self, model: Any) -> List[Issue]:
        issues: List[Issue] = []
        target_elements = model.by_type(self._element_type)

        for element in target_elements:
            if not self._has_valid_attribute(element):
                issues.append(self._create_issue(element))

        return issues

    def _has_valid_attribute(self, element: Any) -> bool:
        if not hasattr(element, self._attribute_name):
            return False

        attribute_value = getattr(element, self._attribute_name)

        if attribute_value is None:
            return False
        if isinstance(attribute_value, str) and not attribute_value.strip():
            return False

        return True

    def _create_issue(self, element: Any) -> Issue:
        return Issue(
            rule_id=self.rule_id,
            element_id=getattr(element, "GlobalId", "UNKNOWN_ID"),
            element_type=element.is_a(),
            message=f"Missing or empty attribute: '{self._attribute_name}'",
            severity=self._severity,
        )
