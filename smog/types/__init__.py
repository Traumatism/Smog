from typing import Type as _Type, Dict

from smog.abstract.command import CommandBase

CommandType = _Type[CommandBase]

from smog.abstract.module import ModuleBase

ModuleType = _Type[ModuleBase]
