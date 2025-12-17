from ponytool.utils.shell import run, check
from ponytool.utils.fs import is_git_repo
from ponytool.utils.ui import success, warn, error

CHECKS = []


def git_doctor(args=None):
    CHECKS.clear()

    if not check_git():
        return
    if not check_repo():
        return

    check_remote()
    check_upstream()
    check_dirty()
    check_branch()

    print_summary()


def check_git() -> bool:
    if check(["git", "--version"]):
        success("Git установлен")
        return True
    error("Git не установлен")
    return False


def check_repo() -> bool:
    if is_git_repo():
        success("Git-репозиторий найден")
        return True
    error("Текущая директория не является git-репозиторием")
    return False


def check_remote():
    remotes = run(["git", "remote"], capture=True).strip()
    if remotes:
        success("Remote origin настроен")
    else:
        warn("Remote не настроен")
        CHECKS.append("remote")


def check_upstream():
    upstream = run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        capture=True,
        check=False
    ).strip()

    if upstream:
        success(f"Upstream: {upstream}")
    else:
        warn("Upstream не найден")
        CHECKS.append("upstream")


def check_dirty():
    dirty = run(["git", "status", "--porcelain"], capture=True).strip()
    if dirty:
        warn("Есть незакоммиченные изменения")
        CHECKS.append("dirty")
    else:
        success("Рабочая директория чистая")


def check_branch():
    branch = run(
        ["git", "branch", "--show-current"],
        capture=True
    ).strip()

    if branch == "main":
        success("Ветка: main")
    else:
        warn(f"Текущая ветка: {branch}")
        CHECKS.append("branch")

RECOMMENDATIONS = {
    "remote": "Добавьте remote: pony git init",
    "upstream": "Настройте upstream: git push -u origin main",
    "dirty": "Закоммитьте изменения перед push",
    "branch": "Рекомендуется использовать ветку main",
}


def print_summary():
    print()
    if not CHECKS:
        success("Git-конфигурация в порядке 🎉")
        return

    warn("Обнаружены проблемы:")
    for key in CHECKS:
        print(f"  • {RECOMMENDATIONS[key]}")
