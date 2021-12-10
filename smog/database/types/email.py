import re

from smog.abstract.type import Type


class Email(Type):
    """ Email type for Smog database """

    name = "email"
    full_name = "emails"
    description = "Email addresses"

    def validate(self) -> bool:
        # regex to validate email
        return re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            self.value
        ) is not None
