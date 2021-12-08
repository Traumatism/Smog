from smog.abstract.command import CommandBase


class Load(CommandBase):
    
    command = "load"
    aliases = ["import"]
    description = "Import database from a smog file"

    def init_arguments(self):
        self.parser.add_argument(
            "file", help="File to import the DB from."
        )

    def execute(self):
        self.database.import_db(self.arguments.file)
