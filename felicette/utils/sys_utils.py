import sys
from rich import print as rprint


def exit_cli(message):
    rprint("%s" % message)
    sys.exit(0)
