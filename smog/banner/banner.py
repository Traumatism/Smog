""" Banner module for Smog """
from smog.logger import console
from smog import __version__

BANNER = r"""[red bold]
              _                     
 _ _  _  _   (_ _ _  _  _    _  _|  
_)|||(_)(_)  | | (_||||(-\)/(_)| |( [green bold]%(version)s[/green bold]
        _/                          
[/red bold]
[cyan bold]a semi automatic osint/recon framework[/cyan bold]
[green bold]author: @toastakerman[/green bold]

"""

class Banner:
    """ Banner class for Smog """
    
    @staticmethod
    def print():
        """ Print the banner to the terminal """
        console.print(BANNER % {"version": __version__}, highlight=False)
