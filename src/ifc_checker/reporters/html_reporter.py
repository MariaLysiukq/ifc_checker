import os
from datetime import datetime
from jinja2 import Template
from ifc_checker.core.interfaces import IReporter
from ifc_checker.core.models import ValidationResult


class HtmlReporter(IReporter):
    """Generates an interactive HTML dashboard using Jinja2 and Bootstrap."""

    def generate(self, result: ValidationResult, output_path: str) -> None:
        error_count = sum(1 for i in result.issues if i.severity.name in ["ERROR", "CRITICAL"])
        warning_count = sum(1 for i in result.issues if i.severity.name == "WARNING")
        info_count = sum(1 for i in result.issues if i.severity.name == "INFO")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "report_template.html")

        with open(template_path, "r", encoding="utf-8") as file:
            template = Template(file.read())
        total = getattr(result, "total_elements", "N/A")
        html_content = template.render(
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            total_elements=total,
            error_count=error_count,
            warning_count=warning_count,
            info_count=info_count,
            issues=result.issues,
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
