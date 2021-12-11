
import time

from smog.logger import Logger
from smog.abstract.module import ModuleBase


class Test(ModuleBase):

    name = "test"
    version = "0.0.1"
    author = "toastakerman"
    description = "Module for testing"
    category = "misc"

    def sub_action(self, i):
        time.sleep(1.5)

    def execute(self):
        for _ in range(15):
            self.respect_threads_run((_, ))

        self.wait_for_finish()
        Logger.success("All actions completed!")
