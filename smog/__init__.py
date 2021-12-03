__version__ = '1.0.0'

from smog.modules.crtsh import CRT
from smog.modules.test import Test
from smog.modules.resolve import Resolve
from smog.modules.hackertarget import HackerTarget

MODULES = (CRT, Test, Resolve, HackerTarget)

from smog.shell import shell
from smog.database import database
