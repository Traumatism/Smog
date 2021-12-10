import re

from smog.abstract.type import Type


class Phone(Type):
    """ Phone number type for Smog database """

    name = "phone"
    full_name = "phones"
    description = "Phone numbers"

    def validate(self) -> bool:
        # regex to validate an universal phone number
        return re.match(
            r"^\+?[0-9]{1,3}\s?\(?[0-9]{3}\)?\s?[0-9]{3}\s?[0-9]{4}$",
            self.value
        ) is not None
