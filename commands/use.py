from smog import MODULES
from smog.logger.logger import Logger
from smog.abstract.command import CommandBase


class Use(CommandBase):

    command = "use"
    description = "Select a module to use"

    def init_arguments(self):
        self.parser.add_argument(
            "module", help="Module name.", choices={module.name for module in MODULES}
        )

    def execute(self):

        module = self.shell.modules_map.get(self.arguments.module, None)

        if module is None:
            return Logger.warn(f"Module '{self.arguments.module}' not found.")

        self.shell.selected_module = module
