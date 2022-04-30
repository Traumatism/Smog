from smog import __version__

__all__ = ("BANNER",)

BANNER = """[red]
   . .
.[yellow]+[/yellow]'|[yellow]=[/yellow]|`[yellow]+[/yellow].
|  | `[yellow]+[/yellow].|
|  | .
`[yellow]+[/yellow].|[yellow]=[/yellow]|`[yellow]+[/yellow].
.    |  |   [yellow]Smog Framework[/yellow]
|`[yellow]+[/yellow]. |  |   [blue]version %(version)s[/blue]
`[yellow]+[/yellow].|[yellow]=[/yellow]|.[yellow]+[/yellow]'

[/red]
[cyan bold]a semi automatic osint/recon framework in Python 🐍[/cyan bold]
[green bold]author: @toastakerman[/green bold]

""" % {
    "version": __version__
}
