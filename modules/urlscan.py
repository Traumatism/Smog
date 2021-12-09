import requests

from smog.abstract.module import ModuleBase
from smog.database.types.url import URL


class UrlScan(ModuleBase):

    name = "urlscan"
    description = "Scan subdomains/IP addresses for HTTP(s) protocols"
    author = "toastakerman"

    keywords = ["urlscan", "url", "scan", "http", "https", "subdomain"]

    def subaction(self, target, scheme):
        try:
            response = requests.get("%s://%s/" % (target, scheme), verify=False, timeout=5)

            self.database.insert_data(URL(response.url))
        except:
            pass


    def execute(self):
        targets = self.database.select_data("subdomains")

        if targets:
            for _, target in targets.items():
                for scheme in ("http", "https"):
                    self.respect_threads_run(args=(target.value, scheme))

        targets = self.database.select_data("ip_addrs") or {}

        if targets:
            for _, target in targets.items():
                self.respect_threads_run(args=(target.value,))

        self.wait_for_finish()
