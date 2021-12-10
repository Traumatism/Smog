import time

from os import system

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import NestedCompleter

from typing import Dict, Union,  Set

from smog import MODULES, COMMANDS, database

from smog.logger import Logger, console
from smog.abstract.module import ModuleBase
from smog.utils.shell import parse_user_input, rich_to_ansi
from smog.types import  ModuleType, CommandType


class Shell:
    """ Shell class for Smog """

    def __init__(self):

        self.selected_module: Union[ModuleBase, None] = None

        self.workspace = None

        # list containing module objects
        self.modules: Set[ModuleType] = MODULES

        # list containing commands objets
        self.commands: Set[CommandType] = COMMANDS

        # dictionnary to convert string to module object
        self.modules_map: Dict[str, ModuleType] = {}

        for module in self.modules:
            self.modules_map[module.name.lower()] = module

        # dictionnary to convert string to command object
        self.commands_map: Dict[str, CommandType] = {}

        for command in self.commands:
            self.commands_map[command.command.lower()] = command

            for alias in command.aliases:
                self.commands_map[alias.lower()] = command

        # setup completer
        json_data = {}

        for command in self.commands_map.values():
            command = command([], self, console, database)

            command.init_arguments()

            json_data[command.command] = {
                argument: None for argument in command.parser.completions
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
            history=InMemoryHistory([command.command for command in self.commands]),
        )

    @property
    def execution_time(self) -> int:
        """ Get last command execution time """
        return round(abs(self.start_time - self.end_time))

    @property
    def prompt(self):
        """ Get shell prompt """
        prompt = "[bold cyan]smog[/bold cyan] "

        if self.selected_module is not None:
            prompt += f"via [bold cyan]{self.selected_module.name}[/bold cyan]"

        if self.execution_time >= 2:
            prompt += f" took [bold cyan]{self.execution_time}s[/bold cyan]"

        prompt += "> "

        return rich_to_ansi(prompt)

    def handle_command_line(self, user_input: str):
        """ Handle user input """
        if bool(user_input) is False:
            return

        if user_input.startswith("!"):
            system(user_input[1:])
            return

        command, arguments = parse_user_input(user_input)

        command_cls = self.commands_map.get(command, None)

        if command_cls is None:
            return Logger.error(f"Unknown command: '{command}'.")

        command = command_cls(arguments, self, console, database)
        command.init_arguments()

        if "-h" in arguments or "--help" in arguments:
            return command.parser.print_help()

        try:
            command.arguments = command.parser.parse_args(command.raw_arguments)
            command.execute()
        except Exception as exc:
            return Logger.error(str(exc))

    def run(self):
        """ Run the shell """

        self.handle_command_line("clear")

        Logger.success("Welcome to [bold cyan]Smog[/bold cyan]! Type 'help' for help.")

        self.start_time = time.time()

        while True:
            self.end_time = time.time()
            user_input = self.prompt_session.prompt(self.prompt)
            self.start_time = time.time()

            self.handle_command_line(user_input)
