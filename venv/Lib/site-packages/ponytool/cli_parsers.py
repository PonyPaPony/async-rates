def git_parser(action_parser):
    action_parser.add_argument(
        "-m", "--message",
        help="Commit message"
    )
    action_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing"
    )
    action_parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Skip confirmations"
    )


def project_parser(action_parser):
    action_parser.add_argument(
        "--no-git",
        action="store_true",
        help="Не инициализировать git-репозиторий"
    )
    action_parser.add_argument(
        "--name",
        help="Имя проекта (будет создана папка)"
    )

def project_clean_parser(action_parser):
    action_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать, что будет удалено, без удаления"
    )
    action_parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Не спрашивать подтверждение"
    )

def run_tests_parser(action_parser):
    action_parser.add_argument(
        "-k",
        help="Фильтр тестов pytest (-k)"
    )

def cov_tests_parser(action_parser):
    action_parser.add_argument(
        '--html',
        action='store_true',
        help="HTML отчёт покрытия"
    )

def git_init_parser(parser):
    parser.add_argument("--remote", help="URL git-репозитория")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    parser.add_argument("-y", "--yes", action="store_true")

def git_rollback_parser(parser):
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Без подтверждений"
    )

def req_generate_parser(parser):
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать requirements.txt без записи"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Перезаписать requirements.txt"
    )
    parser.add_argument(
    "--strict",
    action="store_true",
    help="Ошибка, если есть не сопоставленные импорты или лишние пакеты",
    )

def reg_freeze_parser(parser):
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Не спрашивать подтверждения"
    )

def git_info_parser(parser):
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Показать подробную информацию"
    )
    parser.add_argument(
        "--short",
        action="store_true",
        help="Краткий вывод (для скриптов)"
    )

def req_doctor_parser(parser):
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывести результат в JSON"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Показать подробности"
    )