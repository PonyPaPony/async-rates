from pathlib import Path


def read_metadata(dist_info: Path) -> dict:
    meta_file = dist_info / "METADATA"
    if not meta_file.exists():
        return {}

    name = None
    version = None

    with meta_file.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            name, version = check_startswith(line, name, version)

            if name and version:
                break

    if not name or not version:
        return {}

    return {
        "name": name,
        "version": version,
    }

def check_startswith(line, name, version):
    if line.startswith("Name:"):
        name = line.split(":", 1)[1].strip()
    elif line.startswith("Version:"):
        version = line.split(":", 1)[1].strip()

    return name, version
