from abc import ABC, abstractmethod

from typing import Any

class Type(ABC):
    """" Abstract class for database types """

    name = ""
    full_name = ""
    description = ""

    def __init__(self, value: Any) -> None:
        self.value = value
        self.sub_data = {}

    @abstractmethod
    def validate(self) -> bool:
        """ Validate the value """
