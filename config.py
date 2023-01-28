# Global Environment Configuration

from __future__ import annotations

import os
import re
import copy
import logging
import platform
import multiprocessing
from pathlib import Path
from typing import Callable, Optional, Union
from typing import TYPE_CHECKING

NUM_USABLE_CPU = max(multiprocessing.cpu_count() - 2, 1)

DISK_DATASET_CACHE = "DiskDatasetCache"
SIMPLE_DATASET_CACHE = "SimpleDatasetCache"
DISK_EXPRESSION_CACHE = "DiskExpressionCache"

