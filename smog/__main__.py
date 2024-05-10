import sys

from smog import shell
from smog.logger import Logger

if __name__ == "__main__":
    if len(sys.argv) == 2:
        shell.project_name = sys.argv[1]

    try:
        shell.run()
    except (KeyboardInterrupt, EOFError):
        shell.handle_command_line("quit")
