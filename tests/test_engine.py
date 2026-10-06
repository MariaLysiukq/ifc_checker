from unittest.mock import MagicMock
from ifc_checker.core.engine import ValidationEngine
from ifc_checker.core.interfaces import IIFCModelLoader, IRule
from ifc_checker.core.models import Issue, Severity


class DummyRule(IRule):
    @property
    def rule_id(self) -> str:
        return "TEST_001"

    @property
    def description(self) -> str:
        return "Dummy rule for unit testing"

    def execute(self, model: object) -> list[Issue]:
        return [
            Issue(
                rule_id=self.rule_id,
                element_id="12345",
                element_type="IfcWall",
                message="Missing attribute",
                severity=Severity.ERROR,
            )
        ]


def test_validation_engine_execution() -> None:
    mock_loader = MagicMock(spec=IIFCModelLoader)
    mock_model = [MagicMock(), MagicMock()]
    mock_loader.load.return_value = mock_model

    engine = ValidationEngine(loader=mock_loader)
    engine.register_rule(DummyRule())

    result = engine.validate("dummy_path.ifc")

    assert not result.is_valid
    assert result.total_elements_checked == 2
    assert len(result.issues) == 1
    assert result.issues[0].rule_id == "TEST_001"
