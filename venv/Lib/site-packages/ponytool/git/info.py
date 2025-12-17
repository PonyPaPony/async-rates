from pathlib import Path

from ponytool.utils.shell import run
from ponytool.utils.fs import is_git_repo
from ponytool.utils.ui import info, success, warn, error


def git_info(args):
    if not is_git_repo():
        error("Git-репозиторий не инициализирован")
        return

    root = get_repo_root()
    repo = Path(root).name
    branch = get_branch()
    upstream = get_upstream()
    dirty = is_dirty()

    if args.short:
        print_short(branch, dirty, upstream)
        return

    print_full(repo, root, branch, upstream, dirty, args.verbose)


def get_repo_root() -> str:
    return run(
        ["git", "rev-parse", "--show-toplevel"],
        capture=True
    ).strip()


def get_branch() -> str:
    return run(
        ["git", "branch", "--show-current"],
        capture=True
    ).strip() or "—"


def get_upstream() -> str:
    return run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        capture=True,
        check=False
    ).strip()


def is_dirty() -> bool:
    return bool(run(
        ["git", "status", "--porcelain"],
        capture=True
    ).strip())

def get_remotes() -> dict[str, str]:
    remotes = run(["git", "remote", "-v"], capture=True).strip()
    result = {}

    for line in remotes.splitlines():
        name, url, *_ = line.split()
        result[name] = url

    return result

def print_short(branch, dirty, upstream):
    state = "dirty" if dirty else "clean"
    up = upstream or "no-upstream"
    print(f"{branch} | {state} | {up}")


def print_full(repo, root, branch, upstream, dirty, verbose):
    info(f"Репозиторий: {repo}")
    if verbose:
        info(f"Путь: {root}")

    info(f"Ветка: {branch}")
    print()

    remotes = get_remotes()
    if remotes:
        info("Remote:")
        for name, url in remotes.items():
            print(f"  {name} → {url}")
    else:
        warn("Remote не настроен")

    print()

    if upstream:
        success(f"Upstream: {upstream}")
    else:
        warn("Upstream не найден")

    if dirty:
        warn("Есть незакоммиченные изменения")
    else:
        success("Рабочая директория чистая")
