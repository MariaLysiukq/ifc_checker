import pandas as pd
from ifc_checker.core.interfaces import IReporter
from ifc_checker.core.models import ValidationResult


class ExcelReporter(IReporter):
    def generate(self, result: ValidationResult, output_path: str) -> None:
        if not result.issues:
            df_issues = pd.DataFrame(
                columns=["Rule ID", "Element ID", "Element Type", "Severity", "Message"]
            )
        else:
            issue_data = [
                {
                    "Rule ID": issue.rule_id,
                    "Element ID": issue.element_id,
                    "Element Type": issue.element_type,
                    "Severity": issue.severity.value,
                    "Message": issue.message,
                }
                for issue in result.issues
            ]
            df_issues = pd.DataFrame(issue_data)

        summary_data = {
            "Is Valid": [result.is_valid],
            "Total Elements Checked": [result.total_elements_checked],
            "Total Issues": [len(result.issues)],
        }
        df_summary = pd.DataFrame(summary_data)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_summary.to_excel(writer, sheet_name="Summary", index=False)
            df_issues.to_excel(writer, sheet_name="Issues", index=False)
