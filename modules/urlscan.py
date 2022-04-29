import requests

from smog.abstract.module import ModuleBase
from smog.database.types.url import URL

from urllib3 import disable_warnings

disable_warnings()


class UrlScan(ModuleBase):

    name = "urlscan"
    description = "Scan subdomains/IP addresses for HTTP(s) protocols"
    author = "toastakerman"

    keywords = ["urlscan", "url", "scan", "http", "https", "subdomain"]

    def sub_action(self, target, scheme):
        try:

            requests.get("%s://%s/" % (scheme, target), verify=False, timeout=5)

            self.database.insert_data(URL("%s://%s/" % (scheme, target)))
        except requests.RequestException:
            pass

    def execute(self):
        targets = self.database.select_data("subdomains") or {}

        for _, target in targets.items():
            for scheme in ("http", "https"):
                self.respect_threads_run(args=(target.value, scheme))

        targets = self.database.select_data("ip_addrs") or {}

        for _, target in targets.items():
            for scheme in ("http", "https"):
                self.respect_threads_run(args=(target.value, scheme))
