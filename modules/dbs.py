import socket

from rich.progress import Progress

from smog import module
from smog.database.types.databaseserver import DatabaseServer
from smog.common.module import ABC
from smog.logger import Logger, console

ENGINES = {
    "MySQL": 3306,
    "PgSQL": 5432,
    "MongoDB": 27017,
    "Redis": 6379,
    "Memcached": 11211,
    "MsSQL": 1433,
    "InfluxDB": 8086,
    "Elasticsearch": 9200,
}


@module
class Module(ABC):

    name = "dbs"
    description = "Search for databases servers using port scanning"
    author = "toastakerman"

    def sub_action(self, i, ip, port, engine):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.5)

        try:
            s.connect((ip, port))
        except socket.error:
            return

        Logger.success(f"Found potential {engine} server on '{ip}:{port}'.")

        self.database.update_subdata(
            "ip_addrs",
            i,
            engine.lower(),
            DatabaseServer(
                (ip, port, "null", "null", "null", engine.lower())
            ).export(),
        )

    def execute(self):
        targets = {
            _: target
            for _, target in (
                self.database.select_data("ip_addrs") or {}
            ).items()
            if target.sub_data.get("org", None) != "AS13335 Cloudflare, Inc."
        }

        with Progress(console=console) as progress:
            task = progress.add_task(
                "Scanning for databases",
                total=len(targets) * len(ENGINES.values()),
            )

            for _, target in targets.items():

                for engine, port in ENGINES.items():
                    self.respect_threads_run((_, target.value, port, engine))
                    progress.advance(task, 1)
