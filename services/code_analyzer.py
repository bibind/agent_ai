from pathlib import Path


def list_files(base: str, sub_path: str = ""):
    path = Path(base) / sub_path
    return [p.name for p in path.iterdir()]


def read_file(base: Path, file_path: str) -> str:
    target = Path(base) / file_path
    if target.exists():
        return target.read_text()
    return ""


def write_file(base: Path, file_path: str, content: str):
    target = Path(base) / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
