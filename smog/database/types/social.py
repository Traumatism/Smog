from smog.abstract.type import Type

TYPES = ("instagram.com", "facebook.com", "github.com")


class Social(Type):
    """ Social type """

    name = "social"
    full_name = "socials"
    description = "Social networks"

    def validate(self) -> bool:
        return True
