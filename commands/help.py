from rich.table import Table
from rich.box import SIMPLE

from smog.abstract.command import CommandBase


class Help(CommandBase):

    command = "help"
    description = "Show help menu"
    aliases = ("h", "?")

    def init_arguments(self):
        self.parser.add_argument(
            "-f",
            help="Print full help",
            action="store_true",
            required=False,
            dest="print_full",
        )

    def execute(self):

        if self.arguments.print_full:
            for command in self.shell.commands:

                command_cls = command((), self.shell, self.console, self.database)
                command_cls.init_arguments()

                panel = command_cls.parser.print_help()

                self.console.print(panel)
            return

        table = Table(box=SIMPLE)

        table.add_column("Command", style="bold green")
        table.add_column("Description", style="bold cyan")
        table.add_column("Aliases", style="bold magenta")

        for command in self.shell.commands:
            table.add_row(
                command.command,
                command.description,
                ", ".join(command.aliases) if command.aliases else "-",
            )

        self.console.print(table)
