import json
import os


PATH = os.path.join(os.path.expanduser('~'), '.smog.json')

if not os.path.exists(PATH) or not os.path.isfile(PATH):

    if os.path.exists(PATH):
        os.remove(PATH)

    with open(PATH, "a+") as f:
        f.write("{}")

while True:
    try:
        with open(PATH, "r") as f:
            CONFIG = json.load(f)
            break
    except:
        os.remove(PATH)
        with open(PATH, "a+") as f:
            f.write("{}")


VARIABLES = {
    "prompt_char": (">", ("$", ">", "#", ":")),
    "logging_type": (
        "litteral",
        ("litteral", "symbols", "emojis", "fruits", "nerdfont")
    ),
    "shodan_key": ("null", None),
    "workspace_name": ("default", None),
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
from modules.dbs import Dbs

MODULES = {
    CRT, Test, Resolve, HackerTarget, IPInfo,
    UrlScan, PhpMyAdmin, FullHunt, Dbs
}

from commands.credits import Credits
from commands.select import Select
from commands.delete import Delete
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
    Set, Credits, Quit
}

from smog.shell import shell
