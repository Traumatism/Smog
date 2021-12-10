import requests

from smog.abstract.module import ModuleBase
from smog.database.types.url import URL

from requests.packages.urllib3 import disable_warnings

disable_warnings()


class UrlScan(ModuleBase):

    name = "urlscan"
    description = "Scan subdomains/IP addresses for HTTP(s) protocols"
    author = "toastakerman"

    keywords = ["urlscan", "url", "scan", "http", "https", "subdomain"]

    def subaction(self, target, scheme):
        try:
            response = requests.get("%s://%s/" % (scheme, target), verify=False, timeout=5)
            self.database.insert_data(URL(response.url))
        except Exception as e:
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
                for scheme in ("http", "https"):
                    self.respect_threads_run(args=(target.value, scheme))

        self.wait_for_finish()
