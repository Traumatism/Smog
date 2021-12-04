""" Banner module for Smog. """
from rich.text import Text
from rich.panel import Panel
from rich.box import DOUBLE

from smog import __version__
from smog.logger import console

BANNER = Text(r"""  
  ______________ ________________ _
  __  ___/_  __ `__ \  __ \_  __ `/
 _(__  )_  / / / / / /_/ /  /_/ /
/____/ /_/ /_/ /_/\____/_\__, /
                       /____/ 
""", style="magenta")

A = Panel(Text("""
A semi-automatic osint/recon framework
Version %(version)s
by @toastakerman
"""  % {"author": "toastakerman", "version": __version__}, justify="center"), box=DOUBLE, border_style="magenta")


class Banner:
    """ Banner class for Smog """

    @classmethod
    def print(cls):
      """ Print the banner to the terminal """
      [console.print(i, justify="center") for i in (BANNER, A)]
