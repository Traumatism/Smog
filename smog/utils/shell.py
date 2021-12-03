""" Shell utils for Smog """

from typing import List, Tuple


def parse_user_input(user_input: str) -> Tuple[str, List[str]]:
    """ Parse user input to command name and arguments """
    command, *args = user_input.split()
    return command.lower(), args
