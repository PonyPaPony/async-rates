from ponytool.req.scan.venv import find_venv
from ponytool.req.scan.python import get_python
from ponytool.req.scan.site_packages import get_site_packages
from ponytool.req.scan.collector import collect_installed_packages


def scan():
    venv = find_venv()
    error = check_venv(venv)
    if error:
        return error

    py = get_python()
    python = py['python']
    venv = py['venv']
    error = check_python(python, venv)
    if error:
        return error

    site_packages = get_site_packages(python)
    error = check_site_packages(site_packages, python, venv)
    if error:
        return error

    packages = collect_installed_packages(site_packages)

    return {
        "status": "ok",
        "python": python,
        "venv": venv,
        "packages": packages,
    }

def check_venv(venv):
    if not venv:
        return {
            "status": "no-venv",
            "python": None,
            "venv": None,
            "packages": {},
        }
    return None

def check_python(python, venv):
    if not python:
        return {
            "status": "error",
            "python": None,
            "venv": venv,
            "packages": {},
        }
    return None

def check_site_packages(site_packages, python, venv):
    if not site_packages:
        return {
            "status": "error",
            "python": python,
            "venv": venv,
            "packages": {},
        }
    return None
