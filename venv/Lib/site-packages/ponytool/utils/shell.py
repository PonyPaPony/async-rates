import subprocess


def run(cmd, capture=False, check=True):
    """
    Универсальный shell runner
    """
    if capture:
        return subprocess.check_output(
            cmd,
            text=True,
            stderr=subprocess.STDOUT
        )

    subprocess.run(cmd, check=check)
    return None


def check(cmd):
    """
    Проверка доступности команды
    """
    try:
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except Exception:
        return False
