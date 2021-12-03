""" Banner module for Smog. """
from rich.panel import Panel

from smog import __version__
from smog.logger import console

BANNER = r"""

 .::::::. .        :       ...       .,-:::::/  
;;;`    ` ;;,.    ;;;   .;;;;;;;.  ,;;-'````'   
'[==/[[[[,[[[[, ,[[[[, ,[[     \[[,[[[   [[[[[[/
  '''    $$$$$$$$$"$$$ $$$,     $$$"$$c.    "$$ 
 88b    dP888 Y88" 888o"888,_ _,88P `Y8bo,,,o88o
  "YMmMY" MMM  M'  "MMM  "YMMMMMP"    `'YMUP"YMM [green bold]version %(version)s[/green bold]

[red bold]A semi-automatic osint/recon framework[/red bold]
[cyan bold]by @toastakerman[/cyan bold]
"""


class Banner:
    """ Banner class for Smog """

    @classmethod
    def print(cls):
        """ Print the banner to the terminal """
        console.print(
            Panel.fit(
                BANNER % {"author": "toastakerman", "version": __version__}, 
            ),
            highlight=False, 
            width=100
        )
