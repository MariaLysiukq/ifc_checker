from pathlib import Path
from unittest.mock import MagicMock, patch
from ifc_checker.cli import build_default_engine, main


def test_build_default_engine_registers_rules() -> None:
    engine = build_default_engine()
    assert len(engine._rules) == 3


@patch("ifc_checker.cli.IFCModelLoader")
@patch("ifc_checker.cli.HtmlReporter")
def test_cli_main_execution(
    mock_reporter_cls: MagicMock,
    mock_loader_cls: MagicMock,
    tmp_path: Path,
) -> None:
    dummy_ifc = tmp_path / "sample.ifc"
    dummy_ifc.write_text("ISO-10303-21;")

    mock_loader_inst = MagicMock()
    mock_model = MagicMock()
    mock_model.__iter__.return_value = [MagicMock()]
    mock_model.by_type.return_value = []

    mock_loader_inst.load.return_value = mock_model
    mock_loader_cls.return_value = mock_loader_inst

    mock_reporter_inst = MagicMock()
    mock_reporter_cls.return_value = mock_reporter_inst

    test_args = ["cli.py", str(dummy_ifc), "-o", "out.html", "-f", "html"]
    with patch("sys.argv", test_args):
        main()

    mock_reporter_inst.generate.assert_called_once()
