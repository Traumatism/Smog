""" Shell module for Smog """

import time

from os import system

from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

from typing import Dict, Union, Type, List, Set

from smog.abstract.module import Module
from smog.abstract.command import Command

from smog.database import database
from smog.utils.shell import parse_user_input, rich_to_ansi
from smog.logger import Logger, console
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
from smog.commands.delete import Delete

from smog import MODULES

COMMANDS = {
    Help, Clear,
    Show, Use, Run,
    Select, Add, Delete,
    Python, Credits, Quit
}


class Shell:
    """ Shell class for Smog """

    def __init__(self):
        self.selected_module: Union[Module, None] = None

        self.workspace = None

        self.modules: Set[Type[Module]] = MODULES
        self.commands: Set[Type[Command]] = COMMANDS

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
    def execution_time(self) -> int:
        """ Get last command execution time """
        return round(abs(self.start_time - self.end_time))

    @property
    def prompt(self):
        """ Get shell prompt """
        return rich_to_ansi(
            (
                "\n[bold green]smog[/bold green]"
            ) + (
                f" via [bold green]{self.selected_module.name}({self.selected_module.version})[/bold green]" 
                if self.selected_module is not None else ""
            ) + (
                f" took [bold green]{self.execution_time}s[/bold green]" 
                if self.execution_time >= 2 else ""
            ) + (
                " > "
            )
        )

    def render_status_bar(self):
        """ Status bar """
        return rich_to_ansi(
            f"[green]Module: {self.selected_module.name} v{self.selected_module.version} ({self.selected_module.description})[/green]" 
            if self.selected_module is not None else "[red]No module selected[/red]"
        )

    def run_command(self, command, arguments: List[str] = []):
        """ Run a command """

        # initialize the command
        command = command(arguments, self, console, database)

        try:
            # initialize command arguments
            command.init_arguments()
        except Exception as exc:
            return Logger.warn(str(exc))

        # don't exit the shell if the user asked for the command help
        if "-h" in arguments or "--help" in arguments:
            return command.parser.print_help()

        try:
            
            # parse the arguments
            command.arguments = command.parser.parse_args(command.raw_arguments)
            
            # run the command code
            command.execute()
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

        self.run_command(Clear)

        console.print("[bold green]Run 'help' to see all commands.[/bold green]")

        self.start_time = time.time()

        while True:

            try:
                self.end_time = time.time()

                user_input = prompt(
                    self.prompt, 
                    completer=self.completer, 
                    complete_while_typing=True, 
                    bottom_toolbar=self.render_status_bar
                )

                self.start_time = time.time()

                self.handle_command_line(user_input)

            except (KeyboardInterrupt, EOFError):
                self.run_command(Quit)
                self.start_time = time.time()
