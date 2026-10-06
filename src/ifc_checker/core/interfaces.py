from abc import ABC, abstractmethod
from typing import Any, List
from ifc_checker.core.models import Issue, ValidationResult


class IIFCModelLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> Any:
        pass


class IRule(ABC):
    @property
    @abstractmethod
    def rule_id(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, model: Any) -> List[Issue]:
        pass


class IReporter(ABC):
    @abstractmethod
    def generate(self, result: ValidationResult, output_path: str) -> None:
        pass
