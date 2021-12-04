""" Banner module for Smog. """
from rich.panel import Panel
from rich.columns import Columns

from smog import __version__
from smog.logger import console

BANNER = r"""[magenta]

 .::::::. .        :       ...       .,-:::::/  
;;;`    ` ;;,.    ;;;   .;;;;;;;.  ,;;-'````'   
'[==/[[[[,[[[[, ,[[[[, ,[[     \[[,[[[   [[[[[[/
  '''    $$$$$$$$$"$$$ $$$,     $$$"$$c.    "$$ 
 88b    dP888 Y88" 888o"888,_ _,88P `Y8bo,,,o88o
  "YMmMY" MMM  M'  "MMM  "YMMMMMP"    `'YMUP"YMM 
[/magenta]
"""

A = """
[red bold]A semi-automatic osint/recon framework[/red bold]
[green bold]Version %(version)s[/green bold]
[cyan bold]by @toastakerman[/cyan bold]
"""


class Banner:
    """ Banner class for Smog """

    @classmethod
    def print(cls):
        """ Print the banner to the terminal """
        console.print(
            Columns([BANNER, A % {"author": "toastakerman", "version": __version__}], align="center" ),
            highlight=False, justify="center", style="bold"
        )
