import subprocess
from pathlib import Path
from loguru import logger


def run_script(command: str, cwd: str):
    logger.info(f"Running command in sandbox: {command}")
    proc = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
    logger.info(proc.stdout)
    if proc.returncode != 0:
        logger.error(proc.stderr)
    return proc.stdout
