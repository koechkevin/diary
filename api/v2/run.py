"""
entry point for starting a server
"""
import os
import sys

from __init__ import APP
from models import DatabaseModel

sys.path.insert(0, os.path.abspath(".."))

if __name__ == '__main__':
    DatabaseModel.create_table()
    APP.run(port=5013, debug=True)
    