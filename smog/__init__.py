__version__ = '1.0.0'

from smog.database import database

from smog.modules.crtsh import CRT
from smog.modules.test import Test
from smog.modules.resolve import Resolve

MODULES = (CRT, Test, Resolve)

from smog.shell import shell
