from rich.table import Table
from rich.box import ASCII2

from smog import VARIABLES

from smog.logger import Logger
from smog.common.command import CommandBase


class Show(CommandBase):

    command = "show"
    description = "Show somethin'"

    def init_arguments(self):
        self.parser.add_argument(
            "type",
            help="Thing to show",
            choices=("stats", "modules", "tables", "variables"),
        )

    def execute(self):
        table = Table(box=ASCII2)

        if self.arguments.type == "stats":

            table.add_column("Type", style="bold white")
            table.add_column("%", style="bold white")
            table.add_column("Count", style="bold white")

            try:
                for _table, percents, count in self.database.stats:
                    table.add_row(
                        _table.description.lower(), *map(str, (percents, count))
                    )

            except ZeroDivisionError:
                Logger.error("Database is empty.")

        if self.arguments.type == "modules":

            table.add_column("Module", style="bold white")
            table.add_column("Version", style="bold white")
            table.add_column("Description", style="bold white")
            table.add_column("Author", style="bold white")

            for module in self.shell.modules:
                table.add_row(
                    module.name,
                    module.version,
                    module.description,
                    module.author,
                )

        if self.arguments.type == "variables":

            table.add_column("Variable", style="bold white")
            table.add_column("Value", style="bold white")

            for v, _v in VARIABLES.items():
                table.add_row(v, _v[0])

        if self.arguments.type == "tables":

            table.add_column("Table", style="bold white")
            table.add_column("Description", style="bold white")
            table.add_column("Alias", style="bold white")

            for _table in self.database.tables:
                table.add_row(_table.full_name, _table.description, _table.name)

        return self.console.print(table)
