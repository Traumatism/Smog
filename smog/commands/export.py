import json

from smog.abstract.command import CommandBase


class Export(CommandBase):
    
    command = "export"
    aliases = ["save"]
    description = "Export database to a JSON array"
    
    def execute(self):
        self.console.print(json.dumps(self.database.export_db(), indent=4))
