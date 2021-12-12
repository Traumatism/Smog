""" This is not done yet. """

import pickle

from smog.database.database import Database

from smog import database, VARIABLES


class Workspace:
    """ Workspace class """

    def __init__(self) -> None:
        self.workspace = {
            "name": VARIABLES["workspace_name"],
            "database_b64": database.export_to_data(),
            "variables": VARIABLES
        }

    def refresh(self):
        """ Refresh the workspace """
        self.workspace["name"] = VARIABLES["workspace_name"]
        self.workspace["database_b64"] = database.export_to_data()
        self.workspace["variables"] = VARIABLES

    def export(self):
        self.refresh()

        with open(f"{self.workspace.get('name', 'default')}.smogws", "wb") as file:
            pickle.dump(self.workspace, file)
