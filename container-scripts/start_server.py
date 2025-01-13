import os

from run_shell_command import run_shell_command


def start_server(starbound_install_dir: str):
    start_server_command = [
        os.path.join(starbound_install_dir, "linux", "starbound_server")
    ]

    os.chdir(os.path.join(starbound_install_dir, "linux"))
    run_shell_command(command=start_server_command)
