VARIABLES = {
    "prompt_char": (">", ("$", ">", "#", ":")),
    "logging_type": ("litteral", ("litteral", "symbols", "emojis", "fruits")),
}

__version__ = '1.2.0'

from smog.database import database

from modules.crtsh import CRT
from modules.test import Test
from modules.resolve import Resolve
from modules.hackertarget import HackerTarget
from modules.ipinfo import IPInfo
from modules.urlscan import UrlScan
from modules.phpmyadmin import PhpMyAdmin
from modules.fullhunt import FullHunt


MODULES = {
    CRT, Test, Resolve, HackerTarget, IPInfo, UrlScan, PhpMyAdmin,
    FullHunt
}

from commands.credits import Credits
from commands.select import Select
from commands.delete import Delete
from commands.python import Python
from commands.export import Export
from commands.load import Load
from commands.clear import Clear
from commands.help import Help
from commands.show import Show
from commands.quit import Quit
from commands.use import Use
from commands.run import Run
from commands.add import Add
from commands.set import Set

COMMANDS = {
    Help, Clear,
    Show, Use, Run,
    Select, Add, Delete,
    Export, Load,
    Set,
    Python, Credits, Quit
}

from smog.shell import shell
