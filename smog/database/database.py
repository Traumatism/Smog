import hashlib
import pickle
import base64

from typing import Dict, Iterable, List, Literal, Union, Tuple, Optional
from typing import Type as _Type

from smog.common.type import Type
from smog.logger import Logger

from smog.database.types import (
    Domain,
    IPAddress,
    Port,
    Subdomain,
    URL,
    Email,
    Phone,
    Social,
)

DatabaseType = _Type[Type]
DatabaseDict = Dict[DatabaseType, Dict[int, Type]]


class Database:
    """Primitive database class for Smog"""

    def __init__(self) -> None:

        self.__tables = {
            IPAddress,
            Domain,
            Subdomain,
            URL,
            Email,
            Phone,
            Social,
            Port,
        }

        self.__database: DatabaseDict = {
            table: {} for table in self.__tables if issubclass(table, Type)  # type: ignore
        }

        self.saved = False
        self.last_sum_saved = self.md5sum

    @property
    def md5sum(self) -> str:
        """Return the database md5 sum"""
        return hashlib.md5(pickle.dumps(self.__database)).hexdigest()

    @property
    def is_empty(self) -> bool:
        """Is the database empty?"""
        return not bool(sum((len(_) for _ in self.__database.values())))

    def export_db(self, file: str, quiet: bool):
        """Export database to a file"""

        file += "" if file.endswith(".smog") else ".smog"

        with open(file, "wb") as output:
            pickle.dump(self.__database, output)  # serialize the database

        self.last_sum_saved = self.md5sum

        if not quiet:
            Logger.success(f"Database exported to '{file}'.")

    def import_from_data(self, data: str):
        pass

    def export_to_data(self) -> str:
        """Export the database to a base64 string"""
        return base64.b64encode(pickle.dumps(self.__database)).decode("utf-8")

    def import_db(self, file: str):
        """Import database"""
        Logger.info(f"Importing database from '{file}'...")

        with open(file, "rb") as _input:
            self.__database = pickle.Unpickler(_input).load()

        Logger.success(f"Database imported from '{file}'.")

    @property
    def tables(self) -> List[DatabaseType]:
        """Get the list of tables"""
        return list(self.__database.keys())

    @property
    def stats(self) -> Iterable[Tuple[DatabaseType, Union[float, int], int]]:
        """Get database stats"""
        total = sum(len(i) for i in self.__database.values())

        return [
            (
                table,
                round(len(self.__database[table]) / total * 100),
                len(self.__database[table]),
            )
            for table in self.__database.keys()
        ]

    def get_table_by_str(self, table: str) -> Optional[DatabaseType]:
        """Get table object with full name"""
        return next(
            (
                _table
                for _table in self.tables
                if table in (_table.full_name, _table.name)
            ),
            None,
        )

    def update_subdata(self, table: str, _id: int, key: str, value):
        """Update sub-data from a table"""
        if (_table := self.get_table_by_str(table)) is None:
            return Logger.error("Can't find the table.")

        if _id not in self.__database[_table]:
            return Logger.error(f"Can't find the data for id {_id}.")

        self.__database[_table][_id].sub_data[key] = value

    def delete_data(self, table: str, _id: int):
        """Delete data from a table"""
        if (_table := self.get_table_by_str(table)) is None:
            return Logger.error("Can't find the table.")

        if _id not in self.__database[_table]:
            return Logger.error("Can't find the data.")

        self.__database[_table].pop(_id)

        Logger.success(f"Deleted data from {table} where ID was equal to {_id}.")

    def get_id_by_value(self, value: str) -> int:
        """Get the id of a value"""

        def do_search(table: DatabaseType, value: str):
            items = list(map(lambda k: (k[0], k[1]), self.__database[table].items()))

            return next(
                (_id for _id, data in items if data.value == value),
                None,
            )

        for table in self.tables:
            if (_id := do_search(table, value)) is not None:
                return _id

        return False

    def select_data(
        self, table: str, _id: Optional[int] = None
    ) -> Union[Literal[False], Dict[int, Type]]:
        """Select data from a table"""

        if (_table := self.get_table_by_str(table)) is None:
            return Logger.warn("Can't find the table.")

        return (
            (
                {_id: self.__database[_table][_id]}
                if _id is not None
                else self.__database[_table]
            )
            if _table is not False
            else False
        )

    def insert_data(self, data: Type) -> int | None:
        """Insert data into the table"""

        # data validation
        if data.validate() is False:
            return Logger.warn(f"Can't validate the data: '{data.value}'.")

        if (table := self.get_table_by_str(data.full_name)) is None:
            return Logger.warn("Can't find the table.")

        # don't add data if its already in the database
        for _, j in self.__database[table].items():
            if j.value == data.value:
                return None

        # generate the ID
        _id = (
            max(self.__database[table].keys()) + 1
            if len(self.__database[table]) > 0
            else 1
        )

        self.__database[table][_id] = data  # assign new data to the ID

        Logger.success(f"Added '{data.value}' to {table.full_name}.")

        return _id
