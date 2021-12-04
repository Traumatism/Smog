""" Database module for Smog """

from typing import Dict, List, Literal, Union, Tuple
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

    def export_db(self) -> Dict[_Type[Type], Dict[int, Type]]:
        """ Export database """
        return self.__database

    def import_db(self, database: Dict[_Type[Type], Dict[int, Type]]):
        """ Import database """
        self.__database = database

    @property
    def tables(self) -> List[_Type[Type]]:
        """ Get the list of tables """
        return list(self.__database.keys())

    @property
    def stats(self) -> List[Tuple[_Type[Type], Union[float, int], int]]:
        """ Get database stats """
        total = sum(len(i) for i in self.__database.values())

        return [
            (i, round(len(self.__database[i]) / total * 100), len(self.__database[i])) 
            for i in self.__database.keys()
        ]

    def get_table_by_str(self, table: str) -> Union[Literal[False], _Type[Type]]:
        """ Get table object with full name """
        for _table in self.tables:
            if table in (_table.full_name, _table.name):
                return _table
        return False

    def update_subdata(self, table: str, _id: int, key: str, value):
        """ Update subdata from a table """
        _table = self.get_table_by_str(table)

        if _table is False:
            return Logger.warn("Can't find the table.")

        if _id not in self.__database[_table]:
            return Logger.warn("Can't find the data.")

        self.__database[_table][_id].sub_data[key] = value

    def delete_data(self, table: str, _id: int):
        """ Delete data from a table """
        _table = self.get_table_by_str(table)

        if _table is False:
            return Logger.warn("Can't find the table.")

        if _id not in self.__database[_table]:
            return Logger.warn("Can't find the data.")

        del self.__database[_table][_id]

        Logger.success(f"Deleted data from {table} where ID was equal to {_id}.")

    def get_id_by_value(self, value: str) -> int:
        """ Get the id of a value """
        for table in self.tables:
            for _id, data in self.__database[table].items():
                if data.value == value:
                    return _id
        return False

    def select_data(self, table: str) -> Union[Literal[False], Dict[int, Type]]:
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

        # don't add data if its already in the database
        for _, j in self.__database[table].items():
            if j.value == data.value:
                return

        _id = max(self.__database[table].keys()) + 1 if len(self.__database[table]) > 0 else 1

        self.__database[table][_id] = data

        Logger.success(f"Added '{data.value}' to {table.full_name}.")
