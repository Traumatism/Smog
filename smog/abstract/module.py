import threading as _threading

from abc import ABC, abstractmethod

from smog.database.database import Database
from smog.logger.logger import Logger


class ModuleBase(ABC):
    """" Abstract class for modules """

    name = ""
    version = "0.0.1"
    author = ""
    description = ""
    keywords = []

    def __init__(self, database: Database, threads: int, debug_threads: bool):
        self.database = database
        self.threads = threads
        self.debug_threads = debug_threads

        self.__i = 0

    @abstractmethod
    def subaction(self):
        """ This function gonna be runned with threading """

    def _subaction(self, i, args=[]):
        """ Run subaction """
        if self.debug_threads:
            Logger.info(f"Running subaction #{i}...")

        self.subaction(*args)

        if self.debug_threads:
            Logger.success(f"Subaction #{i} finished.")

    def respect_threads_run(self, args=[]):
        """ Run a function with respect to max threads """
        while 1:
            if _threading.active_count() <= self.threads:
                self.__i += 1
                return _threading.Thread(target=self._subaction, args=(self.__i, args)).start()

    def wait_for_finish(self):
        """ Wait for threads to finish """
        if self.debug_threads:
            Logger.info("Waiting for threads to finish...")

        while _threading.active_count() > 1:
            pass

        self.__i = 0

    def _execute(self):
        self.execute()
        self.wait_for_finish()

    @abstractmethod
    def execute(self):
        """ Execute the module """
