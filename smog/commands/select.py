from rich.table import Table
from rich.box import ASCII2

from smog import database

from smog.abstract.command import Command
from smog.logger.logger import Logger


class Select(Command):

    command = "select"    
    description = "Select datas from the database"

    _arguments = {table.full_name for table in database.tables}

    def init_arguments(self):
        self.parser.add_argument(
            "table", 
            help="Table name.",
            metavar="<table name>"
        )

    def execute(self):
        data = self.database.select_data(self.arguments.table)
        
        if data is False:
            return Logger.warn("Table does not exist.")
        
        if data is []:
            return Logger.warn("Table is empty.")

        table = Table(box=ASCII2)

        table.add_column("#", style="bold bright_black")
        table.add_column("Value", style="bold green")
        table.add_column("Sub-data", style="bold magenta")

        for i, j in data.items():
            table.add_row(str(i), j.value, str(j.sub_data))

        self.console.print(table)
