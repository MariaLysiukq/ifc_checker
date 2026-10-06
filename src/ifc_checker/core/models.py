from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class Issue:
    rule_id: str
    element_id: str
    element_type: str
    message: str
    severity: Severity
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    is_valid: bool
    total_elements_checked: int
    issues: List[Issue] = field(default_factory=list)

    def add_issue(self, issue: Issue) -> None:
        self.issues.append(issue)
        if issue.severity in (Severity.ERROR, Severity.CRITICAL):
            self.is_valid = False
