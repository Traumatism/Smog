import re

from smog.abstract.type import Type


class URL(Type):
    """URL database type"""

    name = "url"
    full_name = "urls"
    description = "URLs"

    def validate(self) -> bool:
        return (
            re.match(
                r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+"
                r"[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$",
                self.value,
            )
            is not None
        )
