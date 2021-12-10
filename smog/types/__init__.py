from typing import Type as _Type

from smog.abstract.module import ModuleBase
from smog.abstract.command import CommandBase

CommandType = _Type[CommandBase] # Command Base Type
ModuleType = _Type[ModuleBase] # Module Base Type
