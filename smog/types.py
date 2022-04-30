from typing import Type

from smog.abstract.module import ModuleBase
from smog.abstract.command import CommandBase

CommandType = Type[CommandBase]  # Command Base Type
ModuleType = Type[ModuleBase]  # Module Base Type
