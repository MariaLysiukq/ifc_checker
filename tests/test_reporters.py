import os
import tempfile
import pandas as pd
from ifc_checker.core.models import ValidationResult, Issue, Severity
from ifc_checker.reporters.excel_reporter import ExcelReporter
from ifc_checker.reporters.html_reporter import HtmlReporter


def _create_dummy_result() -> ValidationResult:
    result = ValidationResult(is_valid=False, total_elements_checked=50)
    result.add_issue(
        Issue(
            rule_id="R01",
            element_id="GUID-12345",
            element_type="IfcWall",
            message="Missing load-bearing property",
            severity=Severity.ERROR,
        )
    )
    return result


def test_excel_reporter_creates_file_with_correct_sheets() -> None:
    reporter = ExcelReporter()
    result = _create_dummy_result()

    with tempfile.TemporaryDirectory() as tmp_dir:
        output_path = os.path.join(tmp_dir, "report.xlsx")
        reporter.generate(result, output_path)

        assert os.path.exists(output_path)

        excel_file = pd.ExcelFile(output_path)
        assert "Summary" in excel_file.sheet_names
        assert "Issues" in excel_file.sheet_names

        df_summary = pd.read_excel(output_path, sheet_name="Summary")
        assert df_summary["Total Issues"].iloc[0] == 1


def test_html_reporter_creates_valid_html_structure() -> None:
    reporter = HtmlReporter()
    result = _create_dummy_result()

    with tempfile.TemporaryDirectory() as tmp_dir:
        output_path = os.path.join(tmp_dir, "report.html")
        reporter.generate(result, output_path)

        assert os.path.exists(output_path)

        with open(output_path, "r", encoding="utf-8") as file:
            content = file.read()

        assert "<h1>IFC Validation Report</h1>" in content
        assert "GUID-12345" in content
        assert "Missing load-bearing property" in content
        assert "Invalid" in content
