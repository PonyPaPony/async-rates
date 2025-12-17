from pathlib import Path
from ponytool.req.scan import metadata

def collect_dist_info(site_packages: Path) -> dict[str, str]:
    packages: dict[str, str] = {}

    for item in site_packages.iterdir():
        if not item.is_dir():
            continue

        if not item.name.endswith(".dist-info"):
            continue

        info = metadata.read_metadata(item)
        if not info:
            continue

        packages[info["name"]] = info["version"]

    return packages