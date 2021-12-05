
from smog.abstract.type import Type


class Email(Type):
    """ Email type for Smog database """

    name = "email"
    full_name = "emails"
    description = "Email addresses"

    def validate(self) -> bool:
        return True
