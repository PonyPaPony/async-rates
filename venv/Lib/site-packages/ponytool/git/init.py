from ponytool.utils.shell import run, check
from ponytool.utils.fs import is_git_repo
from ponytool.utils.ui import info, success, warn, error
from ponytool.utils.io import ask_input, ask_confirm
from pathlib import Path
import shutil
import re


def ensure_git_available():
    if not check(["git", "--version"]):
        error("Git не установлен или недоступен в PATH")
        return False
    return True


def ensure_repo():
    if is_git_repo():
        warn("Git-репозиторий уже существует")
        return False

    info("Инициализация git-репозитория")
    run(["git", "init"])
    return True

def get_remote():
    out = run(["git", "remote"], capture=True).strip()
    return set(out.splitlines())

def ensure_remote(args):
    if get_remote():
        warn("Remote уже настроен — пропускаем")
        return None

    remote = args.remote or ask_input("Введите URL репозитория")

    if not remote:
        error("Remote URL не указан")
        return None

    if not is_valid_remote(remote):
        error("Remote URL выглядит некорректно")
        warn("Примеры:")
        warn("  https://github.com/user/repo.git")
        warn("  git@github.com:user/repo.git")
        return None

    info(f"Remote будет установлен как:\n  {remote}")

    if not args.yes and not ask_confirm("Продолжить?"):
        warn("Настройка remote отменена")
        return None

    try:
        run(["git", "remote", "add", "origin", remote])
        success("Remote origin добавлен")
        return remote
    except Exception:
        error("Не удалось добавить remote")
        warn("Вы можете исправить это командой:")
        warn("  git remote remove origin")
        return None



def initial_commit(args):
    status = run(["git", "status", "--porcelain"], capture=True)

    if not status.strip():
        warn("Нет файлов для коммита")
        return False

    run(["git", "add", "."])
    run(["git", "commit", "-m", "Initial commit"])
    success("Создан первый коммит")
    return True


def initial_push():
    remotes = get_remote()
    if "origin" not in remotes:
        error("Remote origin не найден — push невозможен")
        return

    current = run(
        ["git", "branch", "--show-current"],
        capture=True
    ).strip()

    if current != "main":
        run(["git", "branch", "-M", "main"])
    run(["git", "push", "-u", "origin", "main"])
    success("Репозиторий успешно опубликован 🚀")

def is_valid_remote(remote: str) -> bool:
    return bool(re.match(
        r"^(https://|http://|git@)[\w\.-]+[:/][\w\.-]+/[\w\.-]+(\.git)?$",
        remote
    ))

def rollback_repo():
    git_dir = Path(".git")

    if not git_dir.exists():
        warn("Откат невозможен — .git не найден")
        return

    info("Будет удалён git-репозиторий (.git)")
    warn("Файлы проекта затронуты не будут")

    if not ask_confirm("Продолжить откат?"):
        warn("Откат отменён")
        return

    shutil.rmtree(git_dir)
    success("Git-репозиторий успешно удалён")


def git_init(args):
    if not ensure_git_available():
        return

    if args.rollback:
        rollback_repo()
        return

    if is_git_repo() and get_remote():
        warn("Git-репозиторий и remote уже настроены")
        return

    ensure_repo()

    remote = ensure_remote(args)
    if not remote:
        return

    committed = initial_commit(args)

    if args.no_push:
        warn("Push пропущен (--no-push)")
        return

    if committed or args.yes:
        initial_push()
    else:
        warn("Push пропущен (нет коммита)")
        info("Добавьте файлы и выполните: pony git push")
