import threading as _threading

from abc import ABC, abstractmethod
from typing import Iterable

from smog.database.database import Database
from smog.logger.logger import Logger


class ModuleBase(ABC):
    """ Abstract class for modules """

    name: str = ""
    version: str = "0.0.1"
    author: str = ""
    description: str = ""
    category: str = ""
    keywords: Iterable[str] = []

    def __init__(self, database: Database, threads: int, debug_threads: bool):
        self.debug_threads = debug_threads
        self.database = database
        self.threads = threads

        self.__action = 0

    @abstractmethod
    def sub_action(self, *args):
        """ This function gonna be run with threading """

    def _sub_action(self, i, args=()):
        """ Run sub-action """
        if self.debug_threads:
            Logger.info(f"Running subaction #{i}...")

        self.sub_action(*args)

        if self.debug_threads:
            Logger.success(f"Subaction #{i} finished.")

    def respect_threads_run(self, args: Iterable = []):
        """ Run a function with respect to max threads """
        while 1:
            if _threading.active_count() <= self.threads:
                self.__action += 1
                return _threading.Thread(
                    target=self._sub_action, args=(self.__action, args)
                ).start()

    def wait_for_finish(self):
        """ Wait for threads to finish """
        if self.debug_threads:
            Logger.info("Waiting for threads to finish...")

        while _threading.active_count() > 1:
            pass

        self.__action = 0

    def _execute(self):
        self.execute()
        self.wait_for_finish()

    @abstractmethod
    def execute(self):
        """ Execute the module """
