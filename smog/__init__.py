__version__ = '1.0.0b'

from smog.database import database

from smog.modules.crtsh import CRT
from smog.modules.test import Test
from smog.modules.resolve import Resolve
from smog.modules.hackertarget import HackerTarget
from smog.modules.ipinfo import IPInfo

MODULES = {
    CRT, Test, Resolve, HackerTarget, IPInfo
}

from smog.commands.credits import Credits
from smog.commands.select import Select
from smog.commands.delete import Delete
from smog.commands.python import Python
from smog.commands.export import Export
from smog.commands.clear import Clear
from smog.commands.help import Help
from smog.commands.show import Show
from smog.commands.quit import Quit
from smog.commands.use import Use
from smog.commands.run import Run
from smog.commands.add import Add

COMMANDS = {
    Help, Clear,
    Show, Use, Run,
    Select, Add, Delete, Export,
    Python, Credits, Quit
}


from smog.shell import shell
