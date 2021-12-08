from rich.table import Table
from rich.box import SIMPLE

from smog.logger import Logger
from smog.abstract.command import CommandBase


class Show(CommandBase):

    command = "show"
    description = "Show database tables, modules, or statistics"

    def init_arguments(self):
        self.parser.add_argument(
            "type", help="Data to show", choices=("stats", "modules", "tables")
        )

    def execute(self):
        table = Table(box=SIMPLE)

        if self.arguments.type == "stats":

            table.add_column("Type", style="bold green")
            table.add_column("%", style="bold blue")
            table.add_column("Count", style="bold cyan")

            try:
                for _table, percents, count in self.database.stats:
                    table.add_row(_table.description.lower(), *map(str, (percents, count)))
            except:
                Logger.warn("Database is empty.")

        if self.arguments.type == "modules":

            table.add_column("Module", style="bold green")
            table.add_column("Version", style="bold blue")
            table.add_column("Description", style="bold cyan")
            table.add_column("Author", style="bold magenta")

            for module in self.shell.modules:
                table.add_row(module.name, module.version, module.description, module.author)

        if self.arguments.type == "tables":

            table.add_column("Table", style="bold green")
            table.add_column("Description", style="bold cyan")
            table.add_column("Alias", style="bold magenta")

            for _table in self.database.tables:
                table.add_row(_table.full_name, _table.description, _table.name)

        return self.console.print(table)