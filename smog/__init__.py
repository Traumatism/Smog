import importlib
import glob
import json
import os

from typing import List, Type

PATH = os.path.join(os.path.expanduser("~"), ".smog.json")

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
    except FileExistsError:
        os.remove(PATH)
        with open(PATH, "a+") as f:
            f.write("{}")


VARIABLES = {
    "prompt-char": (">", ("$", ">", "#", ":")),
    "shodan-key": ("null", None),
    "workspace_name": ("default", None),
    "exceptions_debug": ("false", ("false", "true")),
    "user-agent": ("Mozilla/5.0", None),
}

__version__ = "1.3"

from smog.database import database
from smog.common.module import ModuleBase

MODULES: List[Type[ModuleBase]] = []
module = MODULES.append

modules_files = list(
    map(lambda path: "modules." + path[8:][:-3], glob.glob("modules/*.py"))
)


list(map(importlib.import_module, modules_files))

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
from commands.search import Search

COMMANDS = {
    Help,
    Clear,
    Show,
    Use,
    Run,
    Select,
    Add,
    Delete,
    Export,
    Load,
    Set,
    Credits,
    Search,
    Quit,
}

from smog.shell import Shell

shell = Shell()
