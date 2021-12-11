import requests

from smog.abstract.module import ModuleBase
from smog.database.types.subdomain import Subdomain


class FullHunt(ModuleBase):

    name = "fullhunt"
    version = "0.0.1"
    author = "toastakerman"
    description = "Search subdomains on FullHunt.io"

    def sub_action(self, domain):
        with requests.get("https://fullhunt.io/api/v1/domain/%(domain)s/subdomains" % {"domain": domain}) as response:
            json_data = response.json()

        for subdomain in json_data["hosts"]:
            self.database.insert_data(Subdomain(subdomain))

    def execute(self):
        targets = self.database.select_data("domains") or {}

        for _, target in targets.items():
            self.respect_threads_run((target.value,))
