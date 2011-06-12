"""
resources Module

Classes:
Name                               Description
DBMechanic

Exceptions:
None

Functions:
None

Copywrite (c) 2008 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""
from tw.api import CSSLink, Link

#register all the resources in the static directory
CatwalkCss = CSSLink(modname='catwalk', filename='static/css/catwalk.css')
