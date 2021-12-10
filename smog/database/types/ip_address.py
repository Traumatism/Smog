import re

from smog.abstract.type import Type


class IPAddress(Type):
    """ IP address type """

    name = "ip_addr"
    full_name = "ip_addrs"
    description = "IP addresses"

    def validate(self) -> bool:
        return re.match(
            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            self.value
        ) is not None
