""" Database module for Smog """

from typing import Dict, List, Literal, Union, Tuple, Type, Generator

from smog.abstract.type import Type as DatabaseType
from smog.logger.logger import Logger
from smog.database.types import Domain, IPAddress, Subdomain, URL

DatabaseDict = Dict[Type[DatabaseType], Dict[int, DatabaseType]]

class Database:
    """ Primitive database class for Smog """

    def __init__(self) -> None:
        self.__database: DatabaseDict = {
            IPAddress: {},
            Domain: {},
            Subdomain: {},
            URL: {}
        }

    def export_db(self) -> List:
        """ Export database """
        return [
            {database_type.full_name: [row.export() for _, row in content.items()]}
            for database_type, content in self.__database.items()
        ]

    def import_db(self, database: DatabaseDict):
        """ Import database """
        self.__database = database

    @property
    def tables(self) -> List[Type[DatabaseType]]:
        """ Get the list of tables """
        return list(self.__database.keys())

    @property
    def stats(self) -> List[Tuple[Type[DatabaseType], Union[float, int], int]]:
        """ Get database stats """
        total = sum(len(i) for i in self.__database.values())

        return [
            (i, round(len(self.__database[i]) / total * 100), len(self.__database[i])) 
            for i in self.__database.keys()
        ]

    def get_table_by_str(self, table: str) -> Union[Literal[False], Type[DatabaseType]]:
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

    def select_data(self, table: str, _id: int = None) -> Union[Literal[False], Dict[int, DatabaseType]]:
        """ Select data from a table """
        _table = self.get_table_by_str(table)
        
        if _table is False:
            return False
        
        if _id is not None:
            return {_id: self.__database[_table][_id]}

        return self.__database[_table]

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
