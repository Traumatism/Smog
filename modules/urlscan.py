import httpx

from smog.abstract.module import ModuleBase


class UrlScan(ModuleBase):
    
    name = "urlscan"
    description = "Scan subdomains/IP addresses for HTTP(s) protocols"
    author = "toastakerman"
    keywords = ["urlscan", "url", "scan", "http", "https", "ip", "subdomain"]

    def subaction(self, target):
        with httpx.Client() as client:
            try:
                client.get("http://%s/" % target)
                print("ok: %s" % target)
            except:
                print("not ok: %s" % target)


    def execute(self):
        targets = self.database.select_data("subdomains") or []

        for target in targets:
            self.respect_threads_run(args=(target,))
