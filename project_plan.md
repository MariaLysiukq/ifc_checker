# Project Plan: IFC Model Health Checker & COBie Validator

## 1. Project Objective
To build a robust, standalone Python tool that automatically audits IFC (Industry Foundation Classes) files against project-specific BIM requirements (such as EIR/BEP). The tool will identify missing parameters, validate COBie data, detect unassigned geometry, and generate human-readable reports (Excel/HTML) for VDC engineers and BIM coordinators.

## 2. Technology Stack & Rationale

*   **Language:** Python 3.10+
    *   *Why:* The industry standard for data manipulation and automation.
*   **Core BIM Library:** `ifcopenshell`
    *   *Why:* The most powerful open-source library for parsing and modifying IFC geometry and data in Python. It handles schema variations (IFC2x3, IFC4) seamlessly.
*   **Data Processing:** `pandas`
    *   *Why:* Crucial for structuring extracted IFC data into dataframes, making it easy to filter, group, and analyze missing values or duplicate elements.
*   **Reporting:** `openpyxl` (Excel) & `Jinja2` (HTML)
    *   *Why:* BIM coordinators usually work with Excel for issue tracking (BCF is another option, but Excel is the most universal starting point). `Jinja2` allows for creating well-styled, easily readable HTML dashboards.
*   **CLI Interface:** `click` or `argparse`
    *   *Why:* Allows the script to be run easily from the terminal or integrated into CI/CD pipelines (e.g., checking models on upload).
*   **Testing:** `pytest`
    *   *Why:* Aligns with principles to ensure reliability, especially when handling massive, malformed, or unexpected IFC files.

## 3. Step-by-Step Implementation Roadmap

### Phase 1: Project Setup & Infrastructure
*   **Goal:** Establish the repository, virtual environment, and initial file structure.
*   **Tasks:**
    *   Set up standard project directory (`src/`, `tests/`, `docs/`, `data/`).
    *   Define dependencies in `requirements.txt`.
    *   Configure `pytest` and initial testing fixtures (small mock IFC files).

### Phase 2: Core IFC Data Extraction
*   **Goal:** Build the engine that reads the IFC file and extracts necessary elements.
*   **Tasks:**
    *   Implement file loading logic with error handling for corrupted/invalid files.
    *   Create helper functions to extract specific entity types (e.g., `IfcWall`, `IfcDoor`, `IfcBuildingElementProxy`).
    *   Extract Property Sets (Psets) and standard attributes (Name, GlobalId, Type) into a structured Python dictionary or Pandas DataFrame.

### Phase 3: Validation Engine (The "Brain")
*   **Goal:** Implement the logic that checks extracted data against specific rules.
*   **Tasks:**
    *   **Rule 1: Naming Convention Check.** Verify elements follow standard naming (e.g., `[Category]_[Type]_[ID]`).
    *   **Rule 2: COBie Parameter Check.** Verify required properties exist (e.g., `AssetIdentifier`, `Manufacturer`, `SerialNumber`).
    *   **Rule 3: Geometry Check.** Identify "empty" elements (nodes with data but no 3D representation).
    *   **Rule 4: Duplication Check.** Find elements occupying the exact same coordinates or sharing identical GUIDs.

### Phase 4: Reporting Module
*   **Goal:** Output the validation results in a digestible format.
*   **Tasks:**
    *   Format Pandas DataFrames into a clean Excel summary sheet (using `openpyxl` for styling).
    *   Create an HTML template (using `Jinja2`) that displays a high-level summary (e.g., "95% Pass, 5% Fail") and a breakdown of errors by discipline.

### Phase 5: CLI Wrapping & Packaging
*   **Goal:** Make the tool usable for end-users.
*   **Tasks:**
    *   Implement command-line arguments (e.g., `python main.py check --input model.ifc --output report.xlsx --ruleset rules.json`).
    *   Add progress bars or logging so the user knows what is happening during large file processing.

### Phase 6: Edge Cases & Hardening (As per CLAUDE.md)
*   **Goal:** Ensure the tool does not crash on unexpected data.
*   **Tasks:**
    *   Test with empty IFC files, exceptionally large files (>500MB), and files with missing schema headers.
    *   Ensure graceful degradation and clear error messages instead of raw tracebacks.

## 4. Definition of "Done" for MVP
The MVP (Minimum Viable Product) will be considered "done" when a user can run a single command in the terminal, pass an IFC file, and receive an Excel file outlining which elements (by GUID and Name) are missing specific predefined properties. All logic will be backed by passing `pytest` tests.
