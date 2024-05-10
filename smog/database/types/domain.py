import re

from smog.common.type import Type


class Domain(Type):
    """Domain database type"""

    name = "domain"
    full_name = "domains"
    description = "Domains"

    def validate(self) -> bool:
        return (
            re.match(r"^[a-z0-9-]{1,63}(\.[a-z0-9-]{1,63})*$", self.value) is not None
        )
