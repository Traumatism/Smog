from typing import Tuple
from smog.abstract.type import Type
from smog.database.types.email import Email


class Credentials(Type):
    """ Credentials type """

    name = "credential"
    full_name = "credentials"
    description = "Credentials"

    def __init__(self, value: Tuple[Email, str]) -> None:
        super().__init__(value)

    def validate(self) -> bool:
        return True
