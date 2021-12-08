__version__ = '1.0.0b'

from smog.database import database

from modules.crtsh import CRT
from modules.test import Test
from modules.resolve import Resolve
from modules.hackertarget import HackerTarget
from modules.ipinfo import IPInfo

MODULES = {
    CRT, Test, Resolve, HackerTarget, IPInfo
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

COMMANDS = {
    Help, Clear,
    Show, Use, Run,
    Select, Add, Delete, 
    Export, Load,
    Python, Credits, Quit
}

from smog.shell import shell
