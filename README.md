# IFC Model Health Checker & COBie Validator

<div align="center">

![OpenBIM](https://img.shields.io/badge/OpenBIM-IFC2x3%20%7C%20IFC4-0055FF?style=for-the-badge&logo=building&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-SOLID%20%7C%20DDD-green?style=for-the-badge)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge&logo=python)
![Type Checking](https://img.shields.io/badge/Type%20Checker-Mypy%20Strict-blueviolet?style=for-the-badge)

**Automated, lightning-fast, open-source QA/QC & COBie validation tool for BIM/VDC workflows.**

[Key Features](#-key-features) • [Workflow](#-system-workflow) • [Prerequisites](#-prerequisites) • [CLI Reference](#-cli-reference) • [Reporting Engine](#-reporting-engine) • [Extending Rules](#-extending-rules)

---

</div>

>  **Why this tool exists:** Manual BIM QA/QC and COBie compliance checks in Solibri or Navisworks can be time-consuming and costly. This tool provides a **headless, lightweight, and scriptable alternative** using native OpenBIM standards (`ifcopenshell`) to audit models directly in local environments or automated CI/CD pipelines.

---

## Key Features

| Feature | Description | Status |
| :--- | :--- | :---: |
| **OpenBIM Powered** | Native parsing of `.ifc` & `.ifczip` files using `ifcopenshell` without proprietary CAD/BIM software lock-in. | `Ready` |
| **Attribute Validation** | Verifies existence and non-emptiness of core IFC attributes (`Name`, `Description`, `ObjectType`, etc.). | `Ready` |
| **COBie & Pset Auditing** | Deep-inspection of Property Sets (Psets) and custom quantities (e.g., `Pset_WallCommon.LoadBearing`). | `Ready` |
| **Dual Reporting System** | Generates standalone **HTML visual dashboards** or structured **Excel workbooks** for issue tracking. | `Ready` |
| **SOLID Plugin Architecture** | Easily add new custom compliance rules without touching core validation engine code. | `Ready` |
| **CI/CD Ready** | Scriptable CLI returning standard exit codes for automated BIM model integration pipelines. | `Ready` |

---

## System Workflow


```

┌─────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│   IFC Model     │ ───►  │   IFCModelLoader     │ ───►  │   ValidationEngine   │
│ (.ifc / .ifczip)│       └──────────────────────┘       └──────────┬───────────┘
└─────────────────┘                                                 │
▼
┌─────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│  Output Report  │ ◄───  │   IReporter Module   │ ◄───  │   Registered Rules   │
│  (HTML / Excel) │       │ (Html/ExcelReporter) │       │ (Attr / Property)    │
└─────────────────┘       └──────────────────────┘       └──────────────────────┘

```

<details>
<summary><b>🔍 Click to view architectural details (SOLID Principles)</b></summary>

<br>

* **Single Responsibility (SRP):** Each class handles one concern — `IFCModelLoader` loads, `ValidationEngine` orchestrates, rules validate, reporters format.
* **Open/Closed Principle (OCP):** Add new rules by subclassing `IRule` without modifying existing engine logic.
* **Dependency Inversion (DIP):** High-level modules depend on abstractions (`IRule`, `IReporter`, `IIFCModelLoader`), not concrete implementations.
</details>

---

## Prerequisites

Before running the tool, ensure you have:
* **Python 3.10+** installed on your system.
* Target BIM models in **IFC2x3** or **IFC4** format (`.ifc` or `.ifczip`).

---

## CLI Reference

Validate any IFC model directly from your terminal using the global command:

```bash
# Generate an interactive HTML report
ifc-checker path/to/building_model.ifc --output report.html --format html

# Generate a structured Excel spreadsheet for QA management
ifc-checker path/to/building_model.ifc -o cobie_audit.xlsx -f excel

```

### Options Breakdown

| Flag | Short | Type | Default | Description |
| --- | --- | --- | --- | --- |
| `--ifc_file` |  | `string` | *required* | Path to the target `.ifc` file |
| `--output` | `-o` | `string` | `report.html` | Destination path for the output report |
| `--format` | `-f` | `choice` | `html` | Output report format (`html` or `excel`) |

---

## Reporting Engine

The tool offers two built-in reporting mechanisms:

### 1. Interactive HTML Visual Dashboard

Features a clean, modern dashboard highlighting model health status, element breakdown, and color-coded issue severity:

* 🔴 **CRITICAL / ERROR:** Non-compliant attributes or missing required COBie properties.
* 🟡 **WARNING:** Missing non-essential descriptors or recommended attributes.
* 🔵 **INFO:** Informational flags and general metadata.

> 💡 **Self-Contained:** The output is a single `.html` file that can be opened in any browser without external server requirements or internet connectivity.

---

### 2. Excel Spreadsheet Report Structure

Creates a formatted `.xlsx` workbook designed for issue tracking and BIM QA workflows:

1. **`Summary` Sheet:** Overall execution status, total checked elements, compliance score, and breakdown by rule.
2. **`Issues` Sheet:** Itemized audit log containing:
* `Rule ID`
* `Element ID (GlobalId)`
* `Element Type` (e.g., `IfcWall`, `IfcDoor`)
* `Severity`
* `Message / Description`

### 3. BCF 2.1 Native Integration (.bcfzip)

Generates a standardized BIM Collaboration Format (BCF 2.1) zip package for direct feedback loops with design teams:

* `Direct Software Import: Drag and drop .bcfzip into Revit, Navisworks, Archicad, or Solibri.`

* `Automatic Element Isolation: Modeler can click an issue to automatically select and zoom to the exact GlobalId of the non-compliant element.`
    
---

## Extending Rules

Adding a new custom rule to the engine is simple and modular:

```python
from typing import Any, List
from ifc_checker.core.interfaces import IRule
from ifc_checker.core.models import Issue, Severity


class CustomClassificationRule(IRule):
    @property
    def rule_id(self) -> str:
        return "CLASS_001"

    @property
    def description(self) -> str:
        return "Ensures elements have an assigned Uniclass/OmniClass code."

    def execute(self, model: Any) -> List[Issue]:
        issues = []
        # Implement custom OpenBIM logic via ifcopenshell
        return issues

```

Register your new rule in `cli.py` or your custom runner script:

```python
engine.register_rule(CustomClassificationRule())

```
## Docker Support

You can run the checker entirely within an isolated Docker container without needing to install Python or OpenBIM dependencies on your local machine.

### Build the Image
```bash
docker build -t ifc-checker .
```
---

Here is the example of report:
<img width="1886" height="745" alt="зображення" src="https://github.com/user-attachments/assets/81415f49-a9cf-456a-b171-b71034a3f272" />



**Built for OpenBIM & VDC Engineers**
