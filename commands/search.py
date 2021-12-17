from rich.table import Table
from rich.box import SIMPLE

from smog.abstract.command import CommandBase


class Search(CommandBase):

    command = "search"
    description = "Search a module"

    def init_arguments(self):
        self.parser.add_argument("query", help="Query to search")

    def execute(self):
        table = Table(box=SIMPLE)

        table.add_column("Module", style="bold green")
        table.add_column("Version", style="bold blue")
        table.add_column("Description", style="bold cyan")
        table.add_column("Author", style="bold magenta")

        query = self.arguments.query.lower()

        for module in self.shell.modules:
            if query in module.name.lower() or query in module.description.lower():
                table.add_row(
                    module.name,
                    module.version,
                    module.description,
                    module.author
                )

        self.console.print(table)
