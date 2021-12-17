import re

from smog.abstract.type import Type


class Port(Type):
    """ Port type """

    name = "port"
    full_name = "ports"
    description = "Ports"

    def validate(self) -> bool:
        return re.match(
            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):[0-9]{1,5}$",
            self.value
        ) is not None
