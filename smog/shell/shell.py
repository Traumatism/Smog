""" Shell module for Smog """
import time
import re

from os import system

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text.ansi import ANSI
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles.pygments import style_from_pygments_cls

from pygments import token
from pygments.styles.monokai import MonokaiStyle
from pygments.lexer import RegexLexer

from typing import Any, Dict, Optional, Union, Type, List, Set

from smog import MODULES, COMMANDS, database
from smog.logger import Logger, console
from smog.abstract.module import Module
from smog.abstract.command import CommandBase
from smog.utils.shell import parse_user_input, rich_to_ansi


class Shell:
    """ Shell class for Smog """

    def __init__(self):

        self.selected_module: Union[Module, None] = None

        self.workspace = None

        # list containing module objects
        self.modules: Set[Type[Module]] = MODULES
        
        # list containing commands objets
        self.commands: Set[Type[CommandBase]] = COMMANDS

        # dictionnary to convert string to module object
        self.modules_map: Dict[str, Type[Module]] = {}

        for module in self.modules:
            self.modules_map[module.name.lower()] = module

        # dictionnary to convert string to command object
        self.commands_map: Dict[str, Type[CommandBase]] = {}

        for command in self.commands:
            self.commands_map[command.command.lower()] = command

            for alias in command.aliases:
                self.commands_map[alias.lower()] = command

        # setup completer
        json_data = {}

        for command in self.commands_map.values():
            json_data[command.command] = {}

            command = command([], self, console, database)

            command.init_arguments()

            for action_x in command.parser._action_groups:
                for action_y in action_x._group_actions:

                    # add from choices
                    if action_y.choices is not None:
                        for k in action_y.choices:
                            json_data[command.command][k] = None

                    # add from options
                    for action_z in action_y.option_strings:
                        if action_z.startswith("-") is False: # positional arguments
                            continue

                        json_data[command.command][action_z] = None

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
            style=style_from_pygments_cls(MonokaiStyle)
        )

    @property
    def execution_time(self) -> int:
        """ Get last command execution time """
        return round(abs(self.start_time - self.end_time))

    @property
    def prompt(self):
        """ Get shell prompt """
        return rich_to_ansi(
            ("\n[bold cyan]smog[/bold cyan]"
            ) + (f" via [bold cyan]{self.selected_module.name}[/bold cyan]" if self.selected_module is not None else ""
            ) + (f" took [bold cyan]{self.execution_time}s[/bold cyan]" if self.execution_time >= 2 else ""
            ) + " > "
        )

    def run_command(self, command, arguments: List[str] = []):
        """ Run a command """

        # initialize the command
        command = command(arguments, self, console, database)
        command.init_arguments()

        # don't exit the shell if the user asked for the command help
        if "-h" in arguments or "--help" in arguments:
            return command.parser.print_help()

        try:
            command.arguments = command.parser.parse_args(command.raw_arguments) # parse the arguments
            command.execute() # run the command code
        except Exception as exc:
            return Logger.error(str(exc))

    def handle_command_line(self, user_input: str):
        """ Handle user input """
        if bool(user_input) is False:
            return

        # execute system commands
        if user_input.startswith("!"):
            system(user_input[1:])
            return

        command, arguments = parse_user_input(user_input)

        command_cls = self.commands_map.get(command, None)

        if command_cls is None:
            return Logger.error(f"Unknown command: '{command}'.")

        self.run_command(command_cls, arguments)

    def run(self):
        """ Run the shell """

        self.handle_command_line("clear")

        Logger.success("Welcome to [bold cyan]Smog[/bold cyan]! Type 'help' for help.")

        self.start_time = time.time()

        while True:

            try:
                self.end_time = time.time()

                user_input = self.prompt_session.prompt(self.prompt)

                self.start_time = time.time()

                self.handle_command_line(user_input)

            except (KeyboardInterrupt, EOFError):
                self.handle_command_line("quit")
                self.start_time = time.time()

