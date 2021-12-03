from smog.abstract.command import Command
from smog.logger import console

from rich.markdown import Markdown

CREDITS = r'''
# Smog Credits

## Developer 
* toast#3108 (`870366428115640332`)
* github.com/traumatism
* twitter.com/toastakerman

_Concept inspiration: sn0int, github.com/kpcyrd/sn0int_

_Banner inspiration: PwnFunction, youtube.com/PwnFunction_

_Shell inspiration: Spaceship, spaceship-prompt.sh_
'''


class Credits(Command):

    command = "credits"

    description = "Show credits"

    def execute(self):
        console.print(Markdown(CREDITS), width=80)
