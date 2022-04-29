import re

from smog.abstract.type import Type


class Subdomain(Type):
    """Subdomain database"""

    name = "subdomain"
    full_name = "subdomains"
    description = "Subdomains"

    def validate(self) -> bool:
        return (
            re.match(
                r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$",
                self.value,
            )
            is not None
            and self.value.count(".") >= 2
        )
