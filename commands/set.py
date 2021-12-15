from smog.abstract.command import CommandBase
from smog.logger import Logger

from smog import VARIABLES


class Set(CommandBase):

    command = "set"
    description = "Set a variable to a value"

    def init_arguments(self):
        self.parser.add_argument(
            "variable", help="Variable to affect.",
            choices={x for x in VARIABLES.keys()}
        )

        self.parser.add_argument(
            "value", help="Value to set variable to.",
            nargs="*"
        )

    def execute(self):
        value = " ".join(self.arguments.value)
        tmp = VARIABLES[self.arguments.variable][1]

        if tmp is not None and value not in tmp:
            return Logger.error(
                f"Invalid value for variable. (choose from {tmp})"
            )

        VARIABLES[self.arguments.variable] = (value, tmp)

        return Logger.success(f"Variable set to '{value}'")
