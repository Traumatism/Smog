""" Shell module for Smog """

import time

from os import system

from rich.text import Text

from prompt_toolkit import prompt, ANSI
from prompt_toolkit.completion import NestedCompleter

from typing import Dict, Union, Iterable, Type

from smog.abstract.module import Module
from smog.abstract.command import Command

from smog.database import database
from smog.logger import Logger, console
from smog.banner import Banner

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

from smog import MODULES

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

        self.os_commands = {
            "ls", "cd", "pwd", "hostname", "rm",
            "cat", "cp", "mv", "mkdir", "rmdir"
        }

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
            command: {argument + " " for argument in command_cls._arguments}
            for command, command_cls in self.commands_map.items()
        }

        self.c = NestedCompleter.from_nested_dict(json_data)

    @property
    def prompt(self):
        """ Get shell prompt """
        base_prompt = "\n[bold green]smog[/bold green]"

        base_prompt += f" via [bold green]{self.selected_module.name} {self.selected_module.version}[/bold green]" if self.selected_module is not None else ""

        k = round(abs(self.start_time - self.end_time))

        base_prompt += (f" took [bold green]{k}s[/bold green]" if k >= 2 else "") + " > "

        text = Text.from_markup(base_prompt)
        rendered = ""

        for segment in text.render(console):
            if segment.style is None:
                continue

            style = segment.style.copy()

            style._color = segment.style.bgcolor
            style._bgcolor = style.color

            rendered += style.render(segment.text)

        return ANSI(rendered)

    def __parse_user_input(self, user_input: str):
        """ Parse user input to command name and arguments """
        command, *args = user_input.split()
        return command.lower(), args

    def run(self):
        """ Run the shell. """

        Banner.print()

        self.start_time = time.time()

        while True:

            try:
                self.end_time = time.time()

                user_input = prompt(self.prompt, completer=self.c)

                self.start_time = time.time()

                if bool(user_input) is False:
                    continue

                self.command, self.arguments = self.__parse_user_input(user_input)

                if self.command in self.os_commands:
                    Logger.info(f"Executing system command '{user_input}'.")
                    system(user_input)
                    Logger.success("Command executed.")
                    continue

                command_cls = self.commands_map.get(self.command, None)

                if command_cls is None:
                    Logger.warn(f"Unknown command: '{self.command}'.")
                    continue

                try:
                    command_cls = command_cls(self.arguments, self, console, database)
                    command_cls.init_arguments()
                except Exception as exc:
                    Logger.warn(str(exc))
                    continue

                # don't exit the shell if the user asked for the command help
                if "-h" in self.arguments or "--help" in self.arguments:
                    command_cls.parser.print_help()
                    continue

                try:
                    command_cls.arguments = command_cls.parser.parse_args(command_cls.raw_arguments)
                    command_cls.execute()
                except Exception as exc:
                    Logger.warn(str(exc))

            except (KeyboardInterrupt, EOFError):
                Logger.warn("Please use 'quit' command to exit the shell.")
