import dns.resolver

from smog.abstract.module import ModuleBase
from smog.database.types.ip_address import IPAddress


class Spider(ModuleBase):

    name = "spider"
    version = "0.0.1"
    author = "toastakerman"
    description = "Scrape other URLs from URLs"

    def sub_action(self, target: str):
        pass

    def execute(self):
        targets = self.database.select_data("urls") or {}

        for _, target in targets.items():
            self.respect_threads_run((target.value,))
