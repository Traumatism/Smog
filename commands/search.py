from rich.table import Table
from rich.box import ASCII2

from smog.common.command import CommandBase


class Search(CommandBase):

    command = "search"
    description = "Search a module"

    def init_arguments(self):
        self.parser.add_argument("query", help="Query to search")

    def execute(self):
        table = Table(box=ASCII2)

        table.add_column("Module", style="bold white")
        table.add_column("Version", style="bold white")
        table.add_column("Description", style="bold white")
        table.add_column("Author", style="bold white")

        query = self.arguments.query.lower()

        for module in self.shell.modules:
            if query in module.name.lower() or query in module.description.lower():
                table.add_row(
                    module.name,
                    module.version,
                    module.description,
                    module.author,
                )

        self.console.print(table)
