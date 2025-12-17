from ponytool.utils.shell import run
from ponytool.utils.fs import is_git_repo
from ponytool.utils.ui import error


def git_status(args):
    if not is_git_repo():
        error("Текущая директория не является git-репозиторием")
        return

    run(["git", "status"])
