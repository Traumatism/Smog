from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Tuple


class Type(metaclass=ABCMeta):
    """ " Abstract class for database types"""

    name: str = ""
    full_name: str = ""
    description: str = ""

    def __init__(self, value: Any):
        self.value = value
        self.sub_data: Dict[str, Any] = {}

    def export(self) -> Tuple[Any, Dict]:
        """Export the data to a tuple"""
        return self.value, self.sub_data

    @abstractmethod
    def validate(self) -> bool:
        """Validate the value"""
