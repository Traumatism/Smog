from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from rich.box import SIMPLE

from smog.abstract.command import CommandBase
from smog.logger import console


class Help(CommandBase):

    command = "help"
    description = "Show help menu"
    
    aliases = ["h", "?"]

    def execute(self):
        table = Table(box=SIMPLE)

        table.add_column("#", style="bold bright_black")
        table.add_column("Command", style="bold green")
        table.add_column("Description", style="bold cyan")
        table.add_column("Aliases", style="bold magenta")

        for i, command in enumerate(self.shell.commands):
            table.add_row(
                str(i + 1), 
                command.command, 
                command.description, 
                ", ".join(command.aliases) if command.aliases else "-"
            )

        console.print(table)
