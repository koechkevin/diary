import os, sys
sys.path.insert(0, os.path.abspath(".."))

from __init__ import *

from models import DatabaseModel



if __name__ == '__main__':
    DatabaseModel.create_table()
    app.run(port=5003, debug=True)