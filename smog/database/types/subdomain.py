from smog.abstract.type import Type


class Subdomain(Type):
    """ Subdomain database type for Smog """

    name = "subdomain"
    full_name = "subdomains"
    description = "Subdomains"

    def validate(self) -> bool:
        return True
