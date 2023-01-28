name="algoseek"

from importlib.util import find_spec
from pathlib import Path
from pkg_resources import get_distribution, DistributionNotFound


_dist = get_distribution("algoseek")
try:
    # Normalize case for Windows systems
    here = Path(_dist.location) / __file__
    if not here.exists():
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = "Please install this project with setup.py"

version = __version__ = _dist.version

from algoseek.core import *