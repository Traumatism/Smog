import re

from smog.abstract.type import Type


class Email(Type):
    """ Email type """

    name = "email"
    full_name = "emails"
    description = "Email addresses"

    def validate(self) -> bool:
        return re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            self.value
        ) is not None
