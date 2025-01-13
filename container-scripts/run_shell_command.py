import subprocess
import sys
from subprocess import CompletedProcess


def run_shell_command(
    command: str | list[str], allowInput: bool = False
) -> CompletedProcess[str]:
    return subprocess.run(
        command,
        text=True,
        stdin=sys.stdin if allowInput else None,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
