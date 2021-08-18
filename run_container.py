#!/usr/bin/env python3

import sys
from typing import List
from subprocess import run

DEFAULT_DICT_PATH = "/usr/share/dict/web2"

def image_name(dir_name: str):
    return f"bogglesolve-docker-{dir_name}:latest"

def run_bogglesolve_container(dir_name: str, cmd: List[str], dict_path: str = DEFAULT_DICT_PATH):
    full_cmd = [
        "docker", 
        "run", 
        "--rm",
        "--mount", f"type=bind,ro,src={dict_path},dst=/usr/share/dict/words",
        image_name(dir_name),
        *cmd
    ]
    print(' '.join(full_cmd))
    return run(full_cmd, check=True, cwd=f"./{dir_name}", capture_output=True)
    
def main(args):
    proc = run_bogglesolve_container(args[1], args[2:])
    print(proc.stderr.decode('utf8'), file=sys.stderr)
    print(proc.stdout.decode('utf8'))

if __name__ == '__main__':
    main(sys.argv)