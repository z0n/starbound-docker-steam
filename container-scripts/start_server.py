import os
import subprocess


def start_server(starbound_install_dir: str):
    os.chdir(os.path.join(starbound_install_dir, "linux"))
    subprocess.run([os.path.join(starbound_install_dir, "linux", "starbound_server")])
