import dns.resolver

from smog.abstract.module import ModuleBase
from smog.database.types.ip_address import IPAddress
from smog.database.types.subdomain import Subdomain

class Resolve(ModuleBase):

    name = "resolve"
    version = "0.0.1"
    author = "toastakerman"
    description = "Resolve subdomains to IP addresses"
    category = "resolving"

    def subaction(self, target):
        try:
            answers = dns.resolver.query(target, 'A')

            for answer in answers:
                self.database.insert_data(IPAddress(answer.address))

                addr = self.database.select_data("ip_addrs", self.database.get_id_by_value(answer.address)) or answer.address

                if isinstance(addr, str) is False:
                    addr = list(addr.values())[0].export()

                self.database.update_subdata("subdomains", self.database.get_id_by_value(target), "ip_addr", addr)
        except:
            return

    def execute(self):
        targets = self.database.select_data("subdomains") or {}

        for _, target in targets.items():
            self.respect_threads_run((target.value,))
