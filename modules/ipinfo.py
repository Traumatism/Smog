import requests

from smog import module
from smog.common.module import ABC
from smog.database.types.ip_address import IPAddress


@module
class Module(ABC):

    name = "ipinfo"
    version = "0.0.1"
    author = "toastakerman"
    description = "Gather informations on IP addresses"
    category = "scanning"

    def sub_action(self, *args):
        (ip_address,) = args

        with requests.get(f"https://ipinfo.io/{ip_address.value}/json") as response:
            json_data = response.json()

        if response.status_code != 200 or "bogon" in json_data:
            return

        _id = self.database.get_id_by_value(ip_address.value)

        try:
            self.database.update_subdata("ip_addrs", _id, "org", json_data["org"])

            self.database.update_subdata(
                "ip_addrs",
                _id,
                "loc",
                {"country": json_data["country"], "city": json_data["city"]},
            )
        except KeyError:
            pass

    def execute(self):
        targets = self.database.select_data("ip_addrs") or {}

        for _, target in targets.items():
            self.respect_threads_run((target,))
