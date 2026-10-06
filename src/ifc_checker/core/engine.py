from typing import List
from ifc_checker.core.interfaces import IIFCModelLoader, IRule
from ifc_checker.core.models import ValidationResult


class ValidationEngine:
    def __init__(self, loader: IIFCModelLoader) -> None:
        self._loader = loader
        self._rules: List[IRule] = []

    def register_rule(self, rule: IRule) -> None:
        self._rules.append(rule)

    def validate(self, file_path: str) -> ValidationResult:
        model = self._loader.load(file_path)
        total_elements = len(list(model))
        result = ValidationResult(is_valid=True, total_elements_checked=total_elements)

        for rule in self._rules:
            issues = rule.execute(model)
            for issue in issues:
                result.add_issue(issue)

        return result
