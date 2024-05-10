import time
import random

from os import system

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import NestedCompleter

from typing import Dict, FrozenSet, Union, Optional

from smog import MODULES, COMMANDS, VARIABLES, database

from smog.logger import Logger, console
from smog.common.module import ModuleBase
from smog.common.command import CommandBase
from smog.utils.shell import parse_user_input, rich_to_ansi


class Shell:
    """Shell class for Smog"""

    def __init__(self):
        self.selected_module = None
        self.project_name = None

        # list containing module objects
        self.modules = frozenset(
            module for module in MODULES if issubclass(module, ModuleBase)
        )

        # list containing commands objets-
        self.commands = frozenset(
            command for command in COMMANDS if issubclass(command, CommandBase)
        )

        # dictionnary to convert string to module object
        self.modules_map = {module.name.lower(): module for module in self.modules}

        # dictionnary to convert string to command object
        self.commands_map = {}

        for command in self.commands:
            self.commands_map[command.command.lower()] = command

            for alias in command.aliases:
                self.commands_map[alias.lower()] = command

        # setup completer
        json_data = {}

        for command in self.commands_map.values():
            command = command((), self, console, database)
            command.init_arguments()

            json_data[command.command] = dict.fromkeys(command.parser.completions)

            # add from developer-provided arguments
            for argument in command._arguments:
                if argument not in json_data[command.command].keys():
                    json_data[command.command][argument] = None

        self.completer = NestedCompleter.from_nested_dict(json_data)

        # setup prompt
        self.prompt_session = PromptSession(
            completer=self.completer,
            complete_while_typing=True,
            wrap_lines=False,
            history=InMemoryHistory([command.command for command in self.commands]),
        )

    @property
    def execution_time(self) -> int:
        """Get last command execution time"""
        return round(abs(self.start_time - self.end_time))

    @property
    def prompt(self):
        """Get shell prompt"""
        prompt = "[bold white]smog[/]"

        if self.selected_module is not None:
            prompt += f"({self.selected_module.name})"

        if self.execution_time >= 2:
            prompt += f"(took {self.execution_time}s)"

        prompt += f" {VARIABLES['prompt-char'][0]} "

        return rich_to_ansi(prompt)

    def handle_command_line(self, user_input: str) -> None:
        """Handle user input"""
        if not user_input:
            return

        if user_input.startswith("!"):
            system(user_input[1:])
            return

        command, arguments = parse_user_input(user_input)

        if (command_cls := self.commands_map.get(command, None)) is None:
            Logger.error(f"Unknown command: '{command}'.")
            return

        cmd_instance = command_cls(arguments, self, console, database)
        cmd_instance.init_arguments()

        if "-h" in arguments or "--help" in arguments:
            return cmd_instance.parser.print_help()

        try:
            cmd_instance.arguments = cmd_instance.parser.parse_args(arguments)
            cmd_instance.execute()
        except Exception as exc:
            if VARIABLES["exceptions_debug"][0] == "false":
                Logger.error(str(exc))
                return

            return console.print_exception()

    def run(self) -> None:
        """Run the shell"""

        self.handle_command_line("clear -d")  # clear screen
        self.start_time = time.time()

        while True:
            if self.project_name:
                self.handle_command_line(f"export -q {self.project_name}")

            self.end_time = time.time()
            user_input = self.prompt_session.prompt(self.prompt)
            self.start_time = time.time()

            self.handle_command_line(user_input)
