from typing import Literal, Tuple
from smog.abstract.type import Type
from smog.database.types.ip_address import IPAddress
from smog.database.types.credentials import Credentials


class DatabaseServer(Type):
    """ Database  """

    name = "database"
    full_name = "databases"
    description = "Database server"

    def __init__(self, value: Tuple[IPAddress, int, str,  str, str, Literal["mysql", "mssql", "mongodb", "postgresql"]]) -> None:
        super().__init__(value)

    def validate(self) -> bool:
        return True
