#!/bin/python
# Prepend this to your ssh key entry in authorized_keys
# no-port-forwarding,no-x11-forwarding,no-agent-forwarding,command="/path/to/comstop" 
from __future__ import print_function

import ConfigParser
import os
import subprocess
import sys

def report(s):
    print (s, file=sys.stderr)

def get(cp, sect, name, default=""):
    try:
        return cp.get(sect, name)
    except ConfigParser.NoOptionError:
        return default

def main():
    SSH_ORIGINAL_COMMAND=os.environ["SSH_ORIGINAL_COMMAND"].strip()
    CONFIG_FILE=os.path.join(os.environ["HOME"], ".comstop")

    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)

        
    ok = False
    commands = get(config, "DEFAULT", "commands", "")
    for command in commands.split("\n"):
        if SSH_ORIGINAL_COMMAND == command.strip():
            ok = True
            break

    if ok is False:
        report("Denying : " + SSH_ORIGINAL_COMMAND)
        return 1

    run_commands = get(config, "DEFAULT", "run_commands", "0")
    if run_commands != "1":
        report("Ignoring : " + SSH_ORIGINAL_COMMAND)
        return 1

    report("Running : " + SSH_ORIGINAL_COMMAND)

    if get(config, "DEFAULT", "shell", "0") == "1":
        shell = True
    else:
        shell = False
        command = command.split(" ")
    rv = subprocess.call(command, shell=shell)
    return rv

if __name__ == "__main__":
    exit(main())
