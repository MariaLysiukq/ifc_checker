from pathlib import Path
import ifcopenshell
from ifc_checker.core.interfaces import IIFCModelLoader


class IFCModelLoader(IIFCModelLoader):
    def load(self, file_path: str) -> ifcopenshell.file:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"IFC file not found: {file_path}")
        if path.suffix.lower() not in [".ifc", ".ifczip"]:
            raise ValueError(f"Unsupported file extension: {path.suffix}")

        return ifcopenshell.open(str(path))
