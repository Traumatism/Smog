from typing import Tuple, Union

from smog.abstract.type import Type
from smog.database.types.email import Email


class Credentials(Type):
    """Credentials type"""

    name = "credential"
    full_name = "credentials"
    description = "Credentials"

    def __init__(self, value: Tuple[Union[Email, str], str]) -> None:
        super().__init__(value)

    def validate(self) -> bool:
        return True
