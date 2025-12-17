from pathlib import Path
import shutil

from ponytool.utils.fs import is_git_repo
from ponytool.utils.ui import warn, success, info
from ponytool.utils.io import ask_confirm


def git_rollback(args):
    if not is_git_repo():
        warn("Текущая директория не является git-репозиторием")
        return

    git_dir = Path.cwd() / ".git"

    info("Будет удалён git-репозиторий (.git)")
    warn("Файлы проекта затронуты не будут")

    if not args.yes:
        if not ask_confirm("Продолжить откат?"):
            info("Откат отменён")
            return

    shutil.rmtree(git_dir)
    success("Git-репозиторий успешно удалён")
