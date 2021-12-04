from abc import ABC, abstractmethod


class Type(ABC):
    """" Abstract class for database types """

    name = ""
    full_name = ""
    description = ""

    def __init__(self, value) -> None:
        self.sub_data, self.value = {}, value

    @abstractmethod
    def validate(self) -> bool:
        """ Validate the value """
