from pathlib import Path
import shutil

from ponytool.utils.ui import info, warn, success
from ponytool.utils.io import ask_confirm
from ponytool.utils.config import load_config

config = load_config()
TRASH = (
    config
    .get("project", {})
    .get("clean", {})
    .get("trash", [])
)
if not TRASH:
    warn("Список очистки пуст — проверь конфигурацию")

def project_clean(args):
    root = Path.cwd()
    found = []

    for item in TRASH:
        path = root / item
        if path.exists():
            found.append(path)

    if not found:
        info("Нечего очищать — проект чистый")
        return

    info("Будут удалены следующие элементы:")
    for path in found:
        warn(f"  - {path.name}")

    if args.dry_run:
        info("DRY-RUN: удаление не выполняется")
        return

    if not args.yes:
        if not ask_confirm("Продолжить очистку?"):
            info("Очистка отменена")
            return

    for path in found:
        if path.is_dir():
            shutil.rmtree(path)
            success(f"Удалена папка {path.name}")
        else:
            path.unlink()
            success(f"Удалён файл {path.name}")