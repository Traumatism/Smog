import smog.banner

from smog.abstract.command import CommandBase
from smog.logger import console


class Clear(CommandBase):

    command = "clear"
    description = "Clear the screen"
    aliases = ["cls"]

    def init_arguments(self):
        self.parser.add_argument(
            "-d",
            help="Enable banner printing",
            action="store_true",
            required=False,
            dest="print_banner",
        )

    def execute(self):
        console.clear()

        if self.arguments.print_banner:
            console.print(smog.banner.BANNER)
