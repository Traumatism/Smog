from smog import __version__

__all__ = ("BANNER",)

BANNER = r"""
[reset]
 ______     __    __     ______     ______
/\  ___\   /\ "-./  \   /\  __ \   /\  ___\
\ \___  \  \ \ \-./\ \  \ \ \/\ \  \ \ \__ \
 \/\_____\  \ \_\ \ \_\  \ \_____\  \ \_____\
  \/_____/   \/_/  \/_/   \/_____/   \/_____/
[/]
semi automatic recon framework

version: %(version)s

""" % {"version": __version__}
