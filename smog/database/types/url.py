import re

from smog.abstract.type import Type


class URL(Type):
    """ URL database type for Smog """

    name = "url"
    full_name = "urls"
    description = "URLs"

    def validate(self) -> bool:
        return re.match(
            r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$",
            self.value
        ) is not None
