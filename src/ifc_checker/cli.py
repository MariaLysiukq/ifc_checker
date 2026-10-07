import argparse
import sys
from pathlib import Path
from ifc_checker.core.engine import ValidationEngine
from ifc_checker.core.interfaces import IReporter
from ifc_checker.loaders.ifc_loader import IFCModelLoader
from ifc_checker.reporters.excel_reporter import ExcelReporter
from ifc_checker.reporters.html_reporter import HtmlReporter
from ifc_checker.rules.attribute_rule import AttributeExistsRule
from ifc_checker.rules.property_rule import PropertyExistsRule
from ifc_checker.reporters.bcf_reporter import BcfReporter


def build_default_engine() -> ValidationEngine:
    loader = IFCModelLoader()
    engine = ValidationEngine(loader=loader)

    engine.register_rule(
        AttributeExistsRule(
            rule_id="ATTR_001",
            element_type="IfcWall",
            attribute_name="Name",
        )
    )
    engine.register_rule(
        AttributeExistsRule(
            rule_id="ATTR_002",
            element_type="IfcDoor",
            attribute_name="Name",
        )
    )
    engine.register_rule(
        PropertyExistsRule(
            rule_id="PSET_001",
            element_type="IfcWall",
            property_set_name="Pset_WallCommon",
            property_name="LoadBearing",
        )
    )
    return engine


def main() -> None:
    parser = argparse.ArgumentParser(description="IFC Model Health Checker and COBie Validator")
    parser.add_argument("ifc_file", type=str, help="Path to the IFC file")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="report.html",
        help="Path to save the generated report",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["html", "excel", "bcf"],
        default="html",
        help="Report output format (html, excel, or bcf)",
    )

    args = parser.parse_args()

    ifc_path = Path(args.ifc_file)
    if not ifc_path.exists():
        print(f"Error: File '{args.ifc_file}' does not exist.")
        sys.exit(1)

    engine = build_default_engine()
    print(f"Validating '{ifc_path.name}'...")
    result = engine.validate(str(ifc_path))

    reporter: IReporter
    if args.format == "excel":
        reporter = ExcelReporter()
    elif args.format == "bcf":
        reporter = BcfReporter()
    else:
        reporter = HtmlReporter()

    reporter.generate(result, args.output)
    print(f"Validation complete. Report generated at: {args.output}")


if __name__ == "__main__":
    main()
