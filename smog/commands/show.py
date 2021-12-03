from rich.table import Table
from rich.box import SIMPLE

from smog.abstract.command import Command


class Show(Command):

    command = "show"
    description = "Show database tables, modules, or statistics"

    _arguments = {"stats", "modules", "tables"}

    def init_arguments(self):
        self.a = self.parser.add_subparsers(required=True, metavar="tables/modules/stats")

        self.b = self.a.add_parser("tables", help="Show tables.")
        self.c = self.a.add_parser("modules", help="Show modules list.")
        self.d = self.a.add_parser("stats", help="Show database statitics.")

    def execute(self):
        table = Table(box=SIMPLE)

        if self.raw_arguments[0] == "stats":
            table.add_column("#", style="bold bright_black")
            table.add_column("Type", style="bold green")
            table.add_column("%", style="bold blue")
            table.add_column("Count", style="bold cyan")

            for i, (t, p, l) in enumerate(self.database.stats):
                table.add_row(str(i + 1), t.description.lower(), str(p), str(l))

        if self.raw_arguments[0] == "modules":
            table.add_column("#", style="bold bright_black")
            table.add_column("Module", style="bold green")
            table.add_column("Version", style="bold blue")
            table.add_column("Description", style="bold cyan")
            table.add_column("Author", style="bold magenta")

            for i, module in enumerate(self.shell.modules):
                table.add_row(str(i + 1), module.name, module.version, module.description, module.author)

        if self.raw_arguments[0] == "tables":
            table.add_column("#", style="bold bright_black")
            table.add_column("Table", style="bold green")
            table.add_column("Description", style="bold cyan")
            table.add_column("Alias", style="bold magenta")

            for i, j in enumerate(self.database.tables):
                table.add_row(str(i + 1), j.full_name, j.description, j.name)


        return self.console.print(table)
