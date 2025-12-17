from ponytool.utils.shell import run
from ponytool.utils.io import ask_confirm, ask_input
from ponytool.utils.fs import is_git_repo


def git_remove(args):
    if not is_git_repo():
        print("❌ Не git-репозиторий")
        return

    if not ask_confirm("Ты уверен, что хочешь удалить данные git?"):
        print("Отменено")
        return

    choice = ask_input(
        "Что удалить? (branch / repo)",
        default="branch"
    )

    if choice == "branch":
        branch = ask_input("Имя ветки")
        run(["git", "branch", "-D", branch])

    elif choice == "repo":
        run(["git", "clean", "-fd"])
        run(["git", "reset", "--hard"])

    else:
        print("Неизвестный вариант")