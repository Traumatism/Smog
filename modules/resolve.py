import dns.resolver

from smog import module
from smog.common.module import ABC
from smog.database.types.ip_address import IPAddress


@module
class Module(ABC):
    name = "resolve"
    version = "0.0.1"
    author = "toastakerman"
    description = "Resolve subdomains to IP addresses"
    category = "resolving"

    def sub_action(self, target):
        try:
            answers = dns.resolver.resolve(target, "A")

            for answer in answers:
                self.database.insert_data(IPAddress(answer.address))

                addr = (
                    self.database.select_data(
                        "ip_addrs", self.database.get_id_by_value(answer.address)
                    )
                    or answer.address
                )

                if isinstance(addr, str) is False:
                    addr = list(addr.values())[0].export()

                self.database.update_subdata(
                    "subdomains", self.database.get_id_by_value(target), "ip_addr", addr
                )

        except Exception:
            pass

    def execute(self):
        targets = self.database.select_data("subdomains") or {}

        for _, target in targets.items():
            self.respect_threads_run((target.value,))
