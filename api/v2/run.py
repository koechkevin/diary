"""
entry point for starting a server
"""
import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from __init__ import app
from models import DatabaseModel

if __name__ == '__main__':
    DatabaseModel.create_table()
    app.run(port=5013, debug=True)
    