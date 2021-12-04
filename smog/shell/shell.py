""" Shell module for Smog """

import time

from os import system
import rich

from rich.text import Text

from prompt_toolkit import prompt, ANSI
from prompt_toolkit.completion import NestedCompleter

from typing import Dict, Union, Iterable, Type, List

from smog.abstract.module import Module
from smog.abstract.command import Command

from smog.database import database
from smog.logger import Logger, console
from smog.banner import Banner

from smog.utils.shell import parse_user_input, rich_to_ansi

from smog.commands.credits import Credits
from smog.commands.python import Python
from smog.commands.clear import Clear
from smog.commands.help import Help
from smog.commands.show import Show
from smog.commands.use import Use
from smog.commands.run import Run
from smog.commands.select import Select
from smog.commands.add import Add
from smog.commands.quit import Quit

from smog import MODULES, OS_COMMANDS

COMMANDS = {
    Help, Clear,
    Show, Use, Run,
    Select, Add,
    Python, Credits, Quit
}


class Shell:
    """ Shell class for Smog """

    def __init__(self):
        self.selected_module: Union[Module, None] = None

        self.workspace = None

        self.modules: Iterable[Type[Module]] = MODULES
        self.commands: Iterable[Type[Command]] = COMMANDS

        self.modules_map: Dict[str, Type[Module]] = {}
        self.commands_map: Dict[str, Type[Command]] = {}

        for module in self.modules:
            self.modules_map[module.name.lower()] = module

        for command in self.commands:
            self.commands_map[command.command.lower()] = command

            for alias in command.aliases:
                self.commands_map[alias.lower()] = command

        json_data = {
            command: {
                "%s " % argument 
                for argument in command_cls._arguments
            }
            for command, command_cls in self.commands_map.items()
        }

        self.completer = NestedCompleter.from_nested_dict(json_data)

    @property
    def prompt(self):
        """ Get shell prompt """
        base_prompt = "\n[bold green]smog[/bold green]"

        base_prompt += f" via [bold green]{self.selected_module.name}({self.selected_module.version})[/bold green]" if self.selected_module is not None else ""

        k = round(abs(self.start_time - self.end_time))

        base_prompt += (f" took [bold green]{k}s[/bold green]" if k >= 2 else "") + " > "

        return rich_to_ansi(base_prompt)

    def render_status_bar(self):
        return f"Module: {self.selected_module.name} {self.selected_module.version} | {self.selected_module.description}" if self.selected_module is not None else "No module selected"

    def run_command(self, command_cls, arguments: List[str]):
        """ Run a command """
        try:
            command_cls = command_cls(arguments, self, console, database)
            command_cls.init_arguments()
        except Exception as exc:
            return Logger.warn(str(exc))

        # don't exit the shell if the user asked for the command help
        if "-h" in arguments or "--help" in arguments:
            return command_cls.parser.print_help()

        try:
            command_cls.arguments = command_cls.parser.parse_args(command_cls.raw_arguments)
            command_cls.execute()
        except Exception as exc:
            return Logger.warn(str(exc))

    def run(self):
        """ Run the shell """

        self.run_command(Clear, [])

        self.start_time = time.time()

        console.print("[bold green]Run 'help' to see all commands.[/bold green]")

        while True:

            try:
                self.end_time = time.time()

                user_input = prompt(self.prompt, completer=self.completer, complete_while_typing=True, bottom_toolbar=self.render_status_bar)

                self.start_time = time.time()

                if bool(user_input) is False:
                    continue

                command, arguments = parse_user_input(user_input)

                if command in OS_COMMANDS:
                    Logger.info(f"Executing system command '{user_input}'.")
                    system(user_input)
                    Logger.success("Command executed.")
                    continue

                command_cls = self.commands_map.get(command, None)

                if command_cls is None:
                    Logger.warn(f"Unknown command: '{command}'.")
                    continue

                self.run_command(command_cls, arguments)

            except (KeyboardInterrupt, EOFError):
                Logger.warn("Please use 'quit' command to exit the shell.")
                self.start_time = time.time()
