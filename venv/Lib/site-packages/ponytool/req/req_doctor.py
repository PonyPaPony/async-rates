import json
from ponytool.utils.ui import info, success, warn, error

from ponytool.req.doctor_core import run_doctor


def req_doctor(args):
    result = run_doctor()

    if args.json:
        print(json.dumps(_jsonable(result), ensure_ascii=False, indent=2))
        return

    _print_human(result, verbose=args.verbose)


def _print_human(r: dict, verbose: bool):
    # шапка
    if r["ok"]:
        success("Doctor: окружение выглядит нормально")
    else:
        error("Doctor: обнаружены проблемы")

    # базовые пункты
    _line_ok(r["python_ok"], "Python", str(r["python"]), verbose)
    _line_ok(r["venv_ok"], "Venv", str(r["venv"]), verbose)

    if verbose:
        info(f"Site-packages: {len(r['site_packages'])}")
    info(f"Установлено пакетов: {r['installed_packages']}")
    info(f"Импортов найдено: {r['imports']}")
    info(f"Матчей: {r['matched']}")

    unmatched_msg(r)

    # проблемы
    if r["problems"]:
        warn("\nПроблемы:")
        for p in r["problems"]:
            warn(f"  • {p}")

    # подсказки
    if r["hints"]:
        info("\nПодсказки:")
        for h in r["hints"]:
            info(f"  • {h}")


def _line_ok(ok_value, title: str, value: str, verbose: bool):
    if ok_value:
        success(f"{title}: {value}")
    else:
        warn(f"{title}: {value}")


def _jsonable(r: dict) -> dict:
    # Path -> str
    out = dict(r)
    out["python"] = str(out["python"]) if out["python"] else None
    out["venv"] = str(out["venv"]) if out["venv"] else None
    out["site_packages"] = [str(p) for p in out.get("site_packages", [])]
    return out

def unmatched_msg(r):
    if r["unmatched_imports"]:
        warn("\nИмпорты без пакетов:")
        for i in r["unmatched_imports"]:
            warn(f"  • {i}")

    if r["unused_packages"]:
        info("\nНеиспользуемые пакеты:")
        for p in r["unused_packages"]:
            info(f"  • {p}")
