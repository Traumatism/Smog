import contextlib
import requests

from smog import module
from smog.common.module import ABC
from smog.database.types.url import URL

from urllib3 import disable_warnings

disable_warnings()


@module
class Module(ABC):
    name = "urlscan"
    description = "Scan subdomains/IP addresses for HTTP(s) protocols"
    author = "toastakerman"
    keywords = ["urlscan", "url", "scan", "http", "https", "subdomain"]

    def sub_action(self, target, scheme):
        with contextlib.suppress(requests.RequestException):
            response = requests.get(f"{scheme}://{target}/", verify=False, timeout=5)

            _id = self.database.insert_data(URL(f"{scheme}://{target}/"))

            self.database.update_subdata("urls", _id, "body", response.text)
            self.database.update_subdata("urls", _id, "headers", response.headers)

    def execute(self):
        targets = self.database.select_data("subdomains") or {}

        for _, target in targets.items():
            for scheme in ("http", "https"):
                self.respect_threads_run(args=(target.value, scheme))

        targets = self.database.select_data("ip_addrs") or {}

        for _, target in targets.items():
            for scheme in ("http", "https"):
                self.respect_threads_run(args=(target.value, scheme))
