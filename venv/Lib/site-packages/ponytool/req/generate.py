import json
import sys
from pathlib import Path

from ponytool.utils.shell import run
from ponytool.utils.ui import info, success, warn, error
from ponytool.req.scanner import scan
from ponytool.req.imports import collect_imports
from ponytool.req.packages import match_packages
from ponytool.req.writer import write

IGNORED_PACKAGES = {
    "pip",
    "setuptools",
    "wheel"
}


def req_freeze(args):
    info("Генерация requirements.txt")

    python = sys.executable

    # получаем список пакетов
    result = run(
        [python, "-m", "pip", "list", "--format=json"],
        capture=True
    )

    packages = json.loads(result)

    packages = {
        pkg["name"].lower(): pkg["version"]
        for pkg in packages
        if pkg["name"].lower() not in IGNORED_PACKAGES
    }

    write(
        packages=packages,
        path=Path("requirements.txt"),
        dry_run=args.dry_run,
        force=args.yes,
    )

def req_generate(args):
    info("Анализ проекта и генерация requirements.txt")

    info("Сканирование окружения…")
    scan_result = get_scan_result()
    if not scan_result:
        return
    info("Поиск импортов в проекте…")
    imports = get_imports()
    info("Сопоставление пакетов…")
    packages = get_packages(imports, scan_result["packages"])

    unmatched = scan_result.get("unmatched_imports", [])
    unused = scan_result.get("unused_packages", [])

    if args.strict and (unmatched or unused):
        get_unused_unmatched(unmatched, unused)

    write(
        packages=packages,
        path=Path("requirements.txt"),
        dry_run=args.dry_run,
        force=args.force,
    )

def req_clean(args):
    scan_result = scan()
    unused = scan_result.get("unused_packages", [])

    if not unused:
        success("Неиспользуемых пакетов нет")
        return

    warn("Будут удалены пакеты:")
    for p in unused:
        warn(f"  • {p}")

    if not args.yes:
        from ponytool.utils.io import ask_confirm
        if not ask_confirm("Продолжить?"):
            warn("Отменено")
            return

    python = sys.executable
    for pkg in unused:
        run([python, "-m", "pip", "uninstall", "-y", pkg])

    success("Очистка завершена")


def get_scan_result():
    result = scan()
    status = result["status"]
    if status != "ok":
        if status == 'no-venv':
            error("Виртуальное окружение не найдено. Создайте venv.")
        else:
            error("Ошибка анализа окружения")
        return None
    return result

def get_imports():
    imports = collect_imports(Path.cwd())
    if not imports:
        warn("В проекте нет Python-импортов")
        return {}
    return imports

def get_packages(imports, installed_packages):
    packages = match_packages(imports, installed_packages)
    if not packages:
        warn("Зависимости не найдены")
    else:
        success(f"Найдено зависимостей: {len(packages)}")
    return packages

def get_unused_unmatched(unused, unmatched):
        error("Strict mode: обнаружены проблемы")
        if unmatched:
            warn("Импорты без пакетов:")
            for i in unmatched:
                warn(f"  • {i}")
        if unused:
            warn("Неиспользуемые пакеты:")
            for p in unused:
                warn(f"  • {p}")

        return unused, unmatched