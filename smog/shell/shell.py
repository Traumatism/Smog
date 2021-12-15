import time
import random

from os import system

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import NestedCompleter

from typing import Dict, Union,  Set

from smog import (
    MODULES, COMMANDS, VARIABLES, database
)

from smog.logger import Logger, console
from smog.abstract.module import ModuleBase
from smog.abstract.command import CommandBase
from smog.types import ModuleType, CommandType
from smog.utils.shell import parse_user_input, rich_to_ansi


TIPS = (
    "Type 'help' to see a list of available commands.",
    "Use '!command' to run a command in the shell.",
    "If you are using a Nerd Font, you can use 'set logging-type nerdfont'.",
    "Subscribe to my Twitter: @toastakerman :)"
)


class Shell:
    """ Shell class for Smog """

    def __init__(self):
        self.selected_module: Union[ModuleBase, None] = None

        # list containing module objects
        self.modules: Set[ModuleType] = {
            module
            for module in MODULES
            if issubclass(module, ModuleBase)
        }

        # list containing commands objets-
        self.commands: Set[CommandType] = {
            command
            for command in COMMANDS
            if issubclass(command, CommandBase)
        }

        # dictionnary to convert string to module object
        self.modules_map: Dict[str, ModuleType] = {
            module.name.lower(): module
            for module in self.modules
        }

        # dictionnary to convert string to command object
        self.commands_map: Dict[str, CommandType] = {}

        for command in self.commands:
            self.commands_map[command.command.lower()] = command

            for alias in command.aliases:
                self.commands_map[alias.lower()] = command

        # setup completer
        json_data = {}

        for command in self.commands_map.values():
            command = command((), self, console, database)

            command.init_arguments()

            json_data[command.command] = {
                argument: None
                for argument in command.parser.completions
            }

            # add from developer-provided arguments
            for argument in command._arguments:
                if argument not in json_data[command.command].keys():
                    json_data[command.command][argument] = None

        self.completer = NestedCompleter.from_nested_dict(json_data)

        # setup prompt
        self.prompt_session = PromptSession(
            completer=self.completer,
            complete_while_typing=False,
            wrap_lines=False,
            history=InMemoryHistory(
                [command.command for command in self.commands]
            )
        )

    @property
    def execution_time(self) -> int:
        """ Get last command execution time """
        return round(abs(self.start_time - self.end_time))

    @property
    def prompt(self):
        """ Get shell prompt """
        prompt = "([bold cyan]smog[/bold cyan])"

        if self.selected_module is not None:
            prompt += f"([bold cyan]{self.selected_module.name}[/bold cyan])"

        if self.execution_time >= 2:
            prompt += f"([bold cyan]took {self.execution_time}s[/bold cyan])"

        prompt += f" {VARIABLES['prompt-char'][0]} "

        return rich_to_ansi(prompt)

    def handle_command_line(self, user_input: str):
        """ Handle user input """
        if not user_input:
            return

        if user_input.startswith("!"):
            return system(user_input[1:])

        command, arguments = parse_user_input(user_input)

        command_cls = self.commands_map.get(command, None)

        if command_cls is None:
            return Logger.error(f"Unknown command: '{command}'.")

        command = command_cls(arguments, self, console, database)
        command.init_arguments()

        if "-h" in arguments or "--help" in arguments:
            return command.parser.print_help()

        try:
            command.arguments = command.parser.parse_args(arguments)
            command.execute()
        except Exception as exc:
            if VARIABLES["exceptions_debug"] == "false":
                return Logger.error(str(exc))
            return console.print_exception()

    def run(self):
        """ Run the shell """

        self.handle_command_line("clear")  # clear screen

        Logger.info(
            f"{random.choice(TIPS)}\n"
        )

        self.start_time = time.time()

        while True:
            self.end_time = time.time()

            user_input = self.prompt_session.prompt(self.prompt)

            self.start_time = time.time()
            self.handle_command_line(user_input)
