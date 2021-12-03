""" Database module for Smog """

from typing import Dict
from typing import Type as _Type

from smog.abstract.type import Type
from smog.logger.logger import Logger

from smog.database.types import Domain, IPAddress, Subdomain, URL

class Database:
    """ Primitive database class for Smog """

    def __init__(self) -> None:
        self.__database: Dict[_Type[Type], Dict[int, Type]] = {
            IPAddress: {},
            Domain: {},
            Subdomain: {},
            URL: {}
        }

    @property
    def tables(self):
        """ Get the list of tables """
        return list(self.__database.keys())

    @property
    def stats(self):
        """ Get database stats """
        total = sum(len(i) for i in self.__database.values())
        return [(i, round(len(self.__database[i]) / total * 100), len(self.__database[i])) for i in self.__database.keys()]

    def get_table_by_str(self, table: str):
        """ Get table object with full name """
        for _table in self.tables:
            if table in (_table.full_name, _table.name):
                return _table
        return False

    def select_data(self, table: str):
        """ Select data from a table """
        _table = self.get_table_by_str(table)

        return _table if _table is False else self.__database[_table]

    def insert_data(self, data: Type):
        """ Insert data into the table """
        if data.validate() is False:
            return Logger.warn("Can't validate the data.")

        table = self.get_table_by_str(data.full_name)

        if table is False:
            return Logger.warn("Can't find the table.")

        for _, j in self.__database[table].items():
            if j.value == data.value:
                return

        _id = max(self.__database[table].keys()) + 1 if len(self.__database[table]) > 0 else 1

        self.__database[table][_id] = data

        Logger.success(f"Added '{data.value}' to {table.full_name}.")
