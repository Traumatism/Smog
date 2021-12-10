from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table, Row
from rich.box import SIMPLE

from smog.abstract.command import CommandBase
from smog.logger import console


class Help(CommandBase):

    command = "help"
    description = "Show help menu"
    aliases = ("h", "?")

    def execute(self):
        table = Table(box=SIMPLE)

        table.add_column("Command", style="bold green")
        table.add_column("Description", style="bold cyan")
        table.add_column("Aliases", style="bold magenta")

        for command in self.shell.commands:
            table.add_row(command.command, command.description, ", ".join(
                command.aliases) if command.aliases else "-"
            )

        console.print(table)
