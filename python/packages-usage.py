"""
the file structure:

packages-usage.py
subdir1/subdir2/__init__.py
subdir1/subdir2/io_util.py
subdir1/use.py

Usage:
  python packages-usage.py
"""

import os
import sys

# assuming the working dir is always the code repo root dir,
# the import would be always the relative path of root dir no matter where is the py file is,
# e.g. subdir1/use.py
# ```
# from subdir1.subdir2 import io_util
# ```
if os.getcwd() not in sys.path: sys.path.insert(0, os.getcwd())
from subdir1.subdir2 import io_util

fn = 'some_file_path.txt'
content = io_util.get_content(fn)
print(content)
