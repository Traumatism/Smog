from smog.abstract.command import CommandBase
from smog.logger import Logger, console

from smog import database


class Add(CommandBase):

    command = "add"
    aliases = ["insert"]
    description = "Add data to the database."

    def init_arguments(self):

        self.parser.add_argument(
            "table", help="Table to add data to.",
            choices={table.name for table in database.tables}
        )

        self.parser.add_argument(
            "data", help="Data to add."
        )

    def execute(self):
        table = self.database.get_table_by_str(self.arguments.table)

        if table is False:
            return Logger.warn(
                f"Table '{self.arguments.table}' does not exist."
            )

        data = (
            console.input(f"Enter {table.name}: ")
            if self.arguments.data == "?" else self.arguments.data
        )

        self.database.insert_data(table(data))
