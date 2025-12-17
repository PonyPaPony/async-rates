from pathlib import Path

from ponytool.utils.ui import info, success, warn, error
from ponytool.utils.io import ask_confirm
from ponytool.utils.fs import is_git_repo
from ponytool.utils.shell import run
from ponytool.project.gitignore_cfg import GITIGNORE_TEMPLATE

PROJECT_STRUCTURE = [
    "src",
    "tests",
    "docs",
]

def project_init(args):
    base = Path.cwd()

    if args.name:
        root = base / args.name
        if root.exists():
            error(f"Папка '{args.name}' уже существует")
            return
        root.mkdir()
        success(f"Создана папка проекта: {args.name}")
    else:
        root = base

    info(f"Инициализация проекта в {root}")

    # структура проекта
    structure = choice_mode(PROJECT_STRUCTURE)
    creating_process(root, args, structure)

def creating_process(root, args, structure):
    for folder in structure:
        path = root / folder
        if path.exists():
            warn(f"{folder}/ уже существует — пропускаем")
        else:
            ensure_path(path)
            success(f"Создана папка {path.relative_to(root)}")

    # файлы
    create_readme(root)
    create_gitignore(root)

    # git
    if args.no_git:
        warn("Git инициализация отключена (--no-git)")
    else:
        check_repo(root)

def check_repo(root: Path):
    if (root / ".git").exists():
        warn("Git-репозиторий уже существует — пропускаем")
        return

    if ask_confirm("Инициализировать git-репозиторий?"):
        run(["git", "init"], cwd=root)
        success("Git-репозиторий инициализирован")

def create_readme(root):
    readme = root / "README.md"
    if readme.exists():
        warn("README.md уже существует — пропускаем")
        return

    readme.write_text("# Project\n\nОписание проекта.\n", encoding="utf-8")
    success("Создан README.md")

def create_gitignore(root: Path):
    gitignore = root / ".gitignore"
    if gitignore.exists():
        warn(".gitignore уже существует — пропускаем")
        return

    gitignore.write_text(
        GITIGNORE_TEMPLATE,
        encoding="utf-8"
    )
    success("Создан .gitignore")


def choice_mode(default_structure):
    raw = input(
        "Введите структуру папок\n"
        "Примеры:\n"
        "  src,tests,docs\n"
        "  src/api/v1\n"
        "  src,docs/api/v1\n"
        "Нажмите Enter для структуры по умолчанию: "
    ).strip()

    if not raw:
        return [Path(p) for p in default_structure]

    result = []

    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue

        path = normalize_path(part)

        if path.is_absolute() or path.parts[0] in (".", ".."):
            warn(f"Пропущен некорректный путь: {path}")
            continue

        result.append(path)

    return result

def normalize_path(part: str) -> Path:
    return Path(part.replace("\\", "/"))

def normalize_python_file(path: Path) -> Path:
    if path.suffix != ".py":
        path = path.with_suffix(".py")
    return path

def ensure_path(path: Path) -> Path:
    if path.suffix == ".py":
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        return path

    path.mkdir(parents=True, exist_ok=True)
    return path
