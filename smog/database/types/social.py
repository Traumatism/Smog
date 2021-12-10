from smog.abstract.type import Type


class Social(Type):
    """ Credentials type for Smog database """

    name = "social"
    full_name = "socials"
    description = "Social networks"

    def __init__(self, value: str) -> None:
        super().__init__(value)

    def validate(self) -> bool:
        return True
