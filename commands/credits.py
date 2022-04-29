from smog.abstract.command import CommandBase
from smog.logger import console

from rich.markdown import Markdown

CREDITS = r"""
# Smog Credits

## Developer
* toast#3108 (`870366428115640332`)
* github.com/traumatism
* twitter.com/toastakerman

## Others

_Concept -> sn0int, github.com/kpcyrd/sn0int_

_Shell -> Starship, starship.rs_

_Shell bis -> Pwncat, github.com/calebstewart/pwncat/_
"""


class Credits(CommandBase):

    command = "credits"
    description = "Show credits"

    def execute(self):
        console.print(Markdown(CREDITS), width=80)
