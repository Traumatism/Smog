""" Smog abstract classes. """

import threading as _threading

from abc import ABC, abstractmethod

from smog.database.database import Database
from smog.logger.logger import Logger


class Module(ABC):
    """" Abstract class for modules """

    name: str = ""
    version: str = "0.0.1"
    author: str = ""
    category: str = ""
    description: str = ""

    def __init__(self, database: Database, threads: int, debug_threads: bool) -> None:
        self.database = database

        self.debug_threads = debug_threads
        self.threads = threads

        self.__i = 0

    @abstractmethod
    def subaction(self) -> None:
        """ This function gonna be runned with threading """

    def _subaction(self, i, args=[]) -> None:
        """ Run subaction """
        if self.debug_threads:
            Logger.info("Running subaction #%d..." % i)

        self.subaction(*args)

        if self.debug_threads:
            Logger.success("Subaction %d finished." % i)

    def respect_threads_run(self, args=[]) -> None:
        """ Run a function with respect to max threads """
        while 1:
            if _threading.active_count() <= self.threads:
                self.__i += 1
                return _threading.Thread(target=self._subaction, args=(self.__i, args)).start()

    def wait_for_finish(self) -> None:
        """ Wait for threads to finish """
        if self.debug_threads:
            Logger.info("Waiting for threads to finish...")

        while _threading.active_count() > 1:
            pass

        self.__i = 0

    @abstractmethod
    def execute(self) -> None:
        """ Execute the module """

