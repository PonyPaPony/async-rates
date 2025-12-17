from ponytool.utils.shell import run
from ponytool.utils.fs import is_git_repo, has_changes
from ponytool.utils.io import ask_confirm
from ponytool.utils.ui import info, success, error


def git_push(args):
    if not is_git_repo():
        error("Текущая директория не является git-репозиторием")
        return

    run(["git", "status"])

    if not has_changes():
        info("Нет изменений для коммита. Push отменён.")
        return

    interactive = not (args.yes or args.message or args.dry_run)

    if interactive:
        if not ask_confirm("Продолжить коммит и push?"):
            info("Отменено пользователем.")
            return

    message = args.message or "Update"

    if args.dry_run:
        info("DRY-RUN (ничего не выполняется):")
        print("> git add .")
        print(f'> git commit -m "{message}"')
        print("> git push")
        return

    run(["git", "add", "."])
    run(["git", "commit", "-m", message])
    run(["git", "push"])

    success("Push выполнен успешно")
