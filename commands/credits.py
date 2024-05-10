from smog.common.command import CommandBase
from smog.logger import console

from rich.markdown import Markdown

CREDITS = r"""
# Smog Credits

## Developer
* github.com/traumatism

## Others

_Concept -> sn0int, github.com/kpcyrd/sn0int_
"""


class Credits(CommandBase):

    command = "credits"
    description = "Show credits"

    def init_arguments(self):
        pass

    def execute(self):
        console.print(Markdown(CREDITS), width=80)
