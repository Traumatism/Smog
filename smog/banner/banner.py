from smog.logger import console
from smog import __version__

BANNER = """[red]
   . .
.+'|=|`+.
|  | `+.|
|  | .
`+.|=|`+.
.    |  |   [yellow]Smog Framework[/yellow]
|`+. |  |   [blue]version %(version)s[/blue]
`+.|=|.+'

[/red]
[cyan bold]a semi automatic osint/recon framework in Python 🐍[/cyan bold]
[green bold]author: @toastakerman[/green bold]

"""


class Banner:
    """ Banner class """

    @staticmethod
    def print():
        """ Print the banner to the terminal """
        console.print(
            BANNER % {"version": __version__},
            highlight=True
        )
