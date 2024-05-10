import requests

from smog import registery
from smog.common.module import ABC
from smog.database.types.subdomain import Subdomain
from smog.database.types.ip_address import IPAddress


@registery.add_module
class Module(ABC):

    name = "hackertarget"
    version = "0.0.1"
    author = "toastakerman"
    description = "Search subdomains on hackertarget.com"
    keywords = ["hackertarget", "subdomains", "ip addresses", "scanning"]

    def sub_action(self, domain):
        with requests.get(
            "https://api.hackertarget.com/hostsearch/?q=%(domain)s" % {"domain": domain}
        ) as response:
            html_content = response.text

        if "error invalid host" in html_content:
            return

        for line in html_content.splitlines():
            parts = line.split(",")

            self.database.insert_data(Subdomain(parts[0]))
            self.database.insert_data(IPAddress(parts[1]))

    def execute(self):
        targets = self.database.select_data("domains") or {}

        for _, target in targets.items():
            self.respect_threads_run((target.value,))
