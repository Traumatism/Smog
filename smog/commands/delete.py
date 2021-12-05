from smog.abstract.command import CommandBase
from smog.logger import Logger

from smog import database

class Delete(CommandBase):

    command = "delete"
    aliases = ["del", "remove"]
    description = "Remove data from a table."

    _arguments = {table.name for table in database.tables}

    def init_arguments(self):
        self.parser.add_argument("table", help="Table to add data to.", choices={table.name for table in database.tables})
        self.parser.add_argument("id", help="ID of the data to delete.", type=int, metavar="ID")

    def execute(self):
        self.database.delete_data(self.arguments.table, self.arguments.id)
