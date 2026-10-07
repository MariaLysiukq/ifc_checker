from jinja2 import Template
from ifc_checker.core.interfaces import IReporter
from ifc_checker.core.models import ValidationResult


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>IFC Validation Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; color: #333; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .ERROR { color: #d9534f; font-weight: bold; }
        .WARNING { color: #f0ad4e; font-weight: bold; }
        .INFO { color: #5bc0de; }
        .CRITICAL { color: #c9302c; font-weight: bold; }
    </style>
</head>
<body>
    <h1>IFC Validation Report</h1>

    <h2>Summary</h2>
    <ul>
        <li><strong>Status:</strong> {{ "Valid" if result.is_valid else "Invalid" }}</li>
        <li><strong>Elements Checked:</strong> {{ result.total_elements_checked }}</li>
        <li><strong>Total Issues:</strong> {{ result.issues|length }}</li>
    </ul>

    <h2>Issues</h2>
    {% if result.issues %}
    <table>
        <tr>
            <th>Rule ID</th>
            <th>Element ID</th>
            <th>Element Type</th>
            <th>Severity</th>
            <th>Message</th>
        </tr>
        {% for issue in result.issues %}
        <tr>
            <td>{{ issue.rule_id }}</td>
            <td>{{ issue.element_id }}</td>
            <td>{{ issue.element_type }}</td>
            <td class="{{ issue.severity.value }}">{{ issue.severity.value }}</td>
            <td>{{ issue.message }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No issues found. The model is fully compliant with the tested rules.</p>
    {% endif %}
</body>
</html>
"""


class HtmlReporter(IReporter):
    def generate(self, result: ValidationResult, output_path: str) -> None:
        template = Template(HTML_TEMPLATE)
        rendered_html = template.render(result=result)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered_html)
