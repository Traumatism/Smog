import dns.resolver

from smog.abstract.module import Module
from smog.database.types.ip_address import IPAddress

class Resolve(Module):

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
        except:
            return

    def execute(self):
        targets = self.database.select_data("subdomains")

        if targets is False:
            return

        for _, target in targets.items():
            self.respect_threads_run((target.value,))

        self.wait_for_finish()
