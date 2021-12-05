from smog.abstract.type import Type


class Phone(Type):
    """ Phone number type for Smog database """

    name = "phone"
    full_name = "phones"
    description = "Phone numbers"

    def validate(self) -> bool:
        return True
