import ipaddress
import requests

from typing import List

from smog.abstract.type import Type


class IPAddress(Type):
    """ IP address type for Smog database """

    name = "ip_addr"
    full_name = "ip_addrs"
    description = "IP addresses"

    def validate(self) -> bool:
        try:
            ipaddress.IPv4Address(self.value)
            return True
        except:
            return False
