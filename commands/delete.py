import re

from smog.abstract.command import CommandBase


class Delete(CommandBase):

    command = "delete"
    aliases = ("del", "remove")
    description = "Remove data from a table."

    def init_arguments(self):
        self.parser.add_argument(
            "table", help="Table to add data to",
            choices={table.name for table in self.database.tables}
        )

        self.parser.add_argument(
            "id",
            help="ID of the data to delete",
            type=str, metavar="id"
        )

    def test(self):
        """ Testing syntax """
        ids = []

        if re.match(r"\d+<=i<=\d+", self.arguments.id):
            ids = self.arguments.id.split("<=")
            ids = list(map(int, ids))

        if re.match(r"\d+>=i>=\d+", self.arguments.id):
            ids = self.arguments.id.split(">=")
            ids = list(map(int, ids))

        if re.match(r"i==\d+", self.arguments.id):
            ids = self.arguments.id.split("<=")
            ids = list(map(int, ids))

        if re.match(r"i!=\d+", self.arguments.id):
            ids = self.arguments.id.split("!=")

        for i in ids:
            self.database.delete_data(self.arguments.table, i)

    def execute(self):
        self.database.delete_data(self.arguments.table, int(self.arguments.id))
