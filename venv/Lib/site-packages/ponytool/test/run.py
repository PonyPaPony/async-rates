from ponytool.utils.shell import run
from ponytool.utils.ui import info
import sys

def run_tests(args):
    info("Running test")

    python = sys.executable

    cmd = [f"{python}", "-m", "pytest", "--rootdir=."]

    if args.k:
        cmd.extend(["-k", args.k])

    run(cmd)