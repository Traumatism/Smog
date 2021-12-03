import requests

from smog.abstract.module import Module

from smog.database.types.subdomain import Subdomain
from smog.database.types.ip_address import IPAddress

class HackerTarget(Module):

    name = "hackertarget"
    version = "0.0.1"
    author = "toastakerman"
    description = "Search subdomains on hackertarget.com"
    category = "scanning"

    def subaction(self, domain):
        with requests.get("https://api.hackertarget.com/hostsearch/?q=%(domain)s" % {"domain": domain}) as response:
            html_content = response.text

        if 'error invalid host' in html_content:
            return

        for line in html_content.splitlines():
            parts = line.split(',')
            
            self.database.insert_data(Subdomain(parts[0]))
            self.database.insert_data(IPAddress(parts[1]))

    def execute(self):
        targets = self.database.select_data("domains")

        if targets is False:
            return

        for _, target in targets.items():
            self.respect_threads_run((target.value,))

        self.wait_for_finish()
