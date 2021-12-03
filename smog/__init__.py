__version__ = '1.0.0'

from smog.database import database

from smog.modules.crtsh import CRT
from smog.modules.test import Test
from smog.modules.resolve import Resolve
from smog.modules.hackertarget import HackerTarget

MODULES = {CRT, Test, Resolve, HackerTarget}

OS_COMMANDS = {
    "ls", "cd", "pwd", "hostname", "rm",
    "cat", "cp", "mv", "mkdir", "rmdir"
}

from smog.shell import shell
