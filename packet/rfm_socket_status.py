from . import base
from .types import int

class Packeter(base.Packeter):
    status = int.IntType(0, 1)
