from smog.common.command import CommandBase
from smog.logger import Logger


class Export(CommandBase):

    command = "export"
    aliases = ["save"]
    description = "Export database to a .smog file"

    def init_arguments(self):
        self.parser.add_argument("file", help="File to export the DB to")
        self.parser.add_argument(
            "-q", "--quiet", help="Export silently", action="store_true"
        )

    def execute(self):
        if self.database.is_empty is True:
            Logger.warn("The database is empty.")

        self.database.export_db(self.arguments.file, self.arguments.quiet)
