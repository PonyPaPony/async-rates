from ponytool.cli_parsers import *

from ponytool.project.init import project_init
from ponytool.project.clean import project_clean

from ponytool.git.push import git_push
from ponytool.git.status import git_status
from ponytool.git.remove import git_remove
from ponytool.git.init import git_init
from ponytool.git.info import git_info
from ponytool.git.rollback import git_rollback
from ponytool.git.doctor import git_doctor

from ponytool.test.run import run_tests
from ponytool.test.coverage import run_coverage

from ponytool.req.generate import req_generate, req_freeze, req_clean
from ponytool.req.req_doctor import req_doctor

DISPATCH_TABLE = {
    "project": {
        "init": project_init,
        "clean": project_clean,
    },
    "git": {
        'init': git_init,
        'info': git_info,
        "push": git_push,
        "status": git_status,
        "remove": git_remove,
        "rollback": git_rollback,
        "doctor": git_doctor,
    },
    "test": {
        "run": run_tests,
        "coverage": run_coverage,
    },
    "req": {
        'gen': req_generate,
        "freeze": req_freeze,
        "doctor": req_doctor,
        'clean': req_clean,
    }
}

PARSER_TABLE = {
    ("git", "push"): git_parser,
    ("git", 'init'): git_init_parser,
    ('git', 'info'): git_info_parser,
    ("git", 'rollback'): git_rollback_parser,
    ("project", "init"): project_parser,
    ("project", "clean"): project_clean_parser,
    ("test", 'run'): run_tests_parser,
    ("test", 'coverage'): cov_tests_parser,
    ("req", 'gen'): req_generate_parser,
    ('req', 'freeze'): reg_freeze_parser,
    ('req', 'doctor'): req_doctor_parser,
}