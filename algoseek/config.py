"""
Experimental python native configuration file
"""

from datetime import datetime
from typing import Optional, Dict, List
from itertools import chain

class Default:
    """Class for wrapping default values."""

    def __init__(self, value: tp.Any) -> None:
        self.value = value

    def __repr__(self) -> str:
        return "Default(" + self.value.__repr__() + ")"

    def __str__(self) -> str:
        return self.__repr__()

class AlgoSeekSamplesConfig():
    """

    """

    def __init__(self, data_dir="./data"):
        self.data_dir = data_dir

