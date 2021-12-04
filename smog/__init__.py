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

from smog.shell import shell
