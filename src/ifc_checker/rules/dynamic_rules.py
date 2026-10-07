from typing import Any, List
from ifc_checker.core.interfaces import IRule
from ifc_checker.core.models import Issue, Severity


class DynamicPropertyRule(IRule):
    """
    A dynamic rule for checking whether a specific property
    exists in a given Property Set for a specified IFC element type.
    """

    def __init__(
        self, rule_id: str, description: str, entity_type: str, pset_name: str, property_name: str
    ) -> None:
        self._rule_id = rule_id
        self._description = description
        self.entity_type = entity_type
        self.pset_name = pset_name
        self.property_name = property_name

    @property
    def rule_id(self) -> str:
        return self._rule_id

    @property
    def description(self) -> str:
        return self._description

    def execute(self, model: Any) -> List[Issue]:
        issues: List[Issue] = []
        elements = model.by_type(self.entity_type)
        for element in elements:
            has_property = False
            if hasattr(element, "IsDefinedBy"):
                for definition in element.IsDefinedBy:
                    if definition.is_a("IfcRelDefinesByProperties"):
                        property_set = definition.RelatingPropertyDefinition
                        if (
                            property_set.is_a("IfcPropertySet")
                            and property_set.Name == self.pset_name
                        ):
                            for prop in property_set.HasProperties:
                                if prop.Name == self.property_name:
                                    has_property = True
                                    break
                    if has_property:
                        break
            if not has_property:
                issues.append(
                    Issue(
                        rule_id=self.rule_id,
                        element_id=element.GlobalId,
                        element_type=element.is_a(),
                        severity=Severity.ERROR,
                        message=f"Missing property '{self.property_name}' in PSet '{self.pset_name}'",
                    )
                )

        return issues
