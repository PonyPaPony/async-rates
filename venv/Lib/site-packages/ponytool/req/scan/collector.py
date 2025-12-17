from pathlib import Path
from .metadata import read_metadata


EXCLUDE_PACKAGES = {
    "pip",
    "setuptools",
    "wheel",
}


EXCLUDE_PACKAGES = {p.replace("-", "_") for p in EXCLUDE_PACKAGES}


def normalize_name(name: str) -> str:
    return name.lower().replace("-", "_")


def collect_installed_packages(site_packages_dirs: list[Path]) -> dict[str, str]:
    packages: dict[str, str] = {}

    for site_dir in site_packages_dirs:
        for dist_info in site_dir.glob("*.dist-info"):
            meta = read_metadata(dist_info)
            if not meta:
                continue

            name = normalize_name(meta["name"])

            if name in EXCLUDE_PACKAGES:
                continue

            packages[name] = meta["version"]

    return dict(sorted(packages.items()))
