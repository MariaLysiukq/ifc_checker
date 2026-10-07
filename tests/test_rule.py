from unittest.mock import MagicMock
from ifc_checker.core.models import Severity
from ifc_checker.rules.attribute_rule import AttributeExistsRule


def test_attribute_exists_rule_valid_element() -> None:
    rule = AttributeExistsRule("R01", "IfcWall", "Name")

    mock_model = MagicMock()
    valid_element = MagicMock()
    valid_element.is_a.return_value = "IfcWall"
    valid_element.GlobalId = "123"
    valid_element.Name = "Wall-01"

    mock_model.by_type.return_value = [valid_element]

    issues = rule.execute(mock_model)

    assert len(issues) == 0


def test_attribute_exists_rule_missing_attribute() -> None:
    rule = AttributeExistsRule("R01", "IfcWall", "Name", Severity.WARNING)

    mock_model = MagicMock()
    invalid_element = MagicMock()
    invalid_element.is_a.return_value = "IfcWall"
    invalid_element.GlobalId = "456"
    invalid_element.Name = ""

    mock_model.by_type.return_value = [invalid_element]

    issues = rule.execute(mock_model)

    assert len(issues) == 1
    assert issues[0].rule_id == "R01"
    assert issues[0].severity == Severity.WARNING
    assert "Missing or empty attribute" in issues[0].message
