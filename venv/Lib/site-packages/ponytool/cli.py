import argparse

from ponytool.utils.ui import error, info
from ponytool.cli_parsers import *
from ponytool.cli_config import *


def main():
    parser = argparse.ArgumentParser(prog="pony")
    subparsers = parser.add_subparsers(dest="command")

    for section, actions in DISPATCH_TABLE.items():
        section_parser = subparsers.add_parser(section)
        section_sub = section_parser.add_subparsers(dest="action")

        for action in actions:
            action_parser = section_sub.add_parser(action)

            parser_func = PARSER_TABLE.get((section, action))
            if parser_func:
                parser_func(action_parser)

    args = parser.parse_args()
    dispatch(args)

def dispatch(args):
    if not args.command:
        run_interactive_menu()
        return

    if args.command not in DISPATCH_TABLE:
        error(f"Неизвестная команда: {args.command}")
        return

    if not args.action:
        print_section_help(args.command)
        return

    handler = DISPATCH_TABLE[args.command].get(args.action)

    if not handler:
        print_action_help(args.command)
        return

    handler(args)

def print_section_help(section: str):
    info(f"\nДоступные действия для '{section}':")
    for action in DISPATCH_TABLE[section]:
        info(f"  - {action}")

def print_action_help(section: str):
    info(f"\nНеизвестное действие для '{section}'.")
    print_section_help(section)

def run_interactive_menu():
    info("\nPonyTool — интерактивный режим\n")

    for section, actions in DISPATCH_TABLE.items():
        info(section)
        for action in actions:
            info(f"  - {action}")

    info("\nПример: pony git push")

if __name__ == '__main__':
    main()
