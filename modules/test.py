import time

from smog.abstract.module import ModuleBase


class Test(ModuleBase):

    name = "test"
    version = "0.0.1"
    author = "toastakerman"
    description = "Module for testing"
    category = "misc"

    def sub_action(self, i):
        """ This function gonna be executed in a thread """
        time.sleep(1)

    def execute(self):
        for _ in range(15):

            # This built-in function will spawn a new thread of
            # 'self.sub_action' with respect to the number of
            # threads specified
            self.respect_threads_run((_, ))
