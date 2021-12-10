from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


class Type(ABC):
    """" Abstract class for database types """

    name = ""
    full_name = ""
    description = ""

    def __init__(self, value: Any):
        self.value = value
        self.sub_data = {}

    def export(self) -> Tuple[Any, Dict]:
        """ Export the data to a tuple """
        return (self.value, self.sub_data)

    @abstractmethod
    def validate(self) -> bool:
        """ Validate the value """
