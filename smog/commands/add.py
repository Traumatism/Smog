from smog.abstract.command import Command
from smog.logger import Logger

from smog import database

class Add(Command):

    command = "add"
    aliases = ["insert"]
    description = "Insert data into the database"

    _arguments = {table.name for table in database.tables}

    def init_arguments(self):
        self.parser.add_argument("table", help="Table to add data to.")
        self.parser.add_argument("data", help="Data to add.")

    def execute(self):
        table = self.database.get_table_by_str(self.arguments.table)

        if table is False:
            return Logger.warn(f"Table '{self.arguments.table}' does not exist.")

        self.database.insert_data(table(self.arguments.data))
