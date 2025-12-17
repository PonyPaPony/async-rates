from ponytool.utils.shell import run
from ponytool.utils.ui import info
import sys


def run_coverage(args):
    info("Running coverage test")

    python = sys.executable

    cmd = [f"{python}", "-m", "pytest", "--rootdir=.", "--cov"]

    if args.html:
        cmd.append('--cov-report=html')
    else:
        cmd.append('--cov-report=term')

    run(cmd)