from typing import Type

from smog.common.module import ModuleBase
from smog.common.command import CommandBase

CommandType = Type[CommandBase]  # Command Base Type
ModuleType = Type[ModuleBase]  # Module Base Type
