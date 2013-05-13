import sqlalchemy
import os
import sys

from atrium_fetch.util import dieIf
from atrium_fetch.db import *

def commandInit(args, dummy):
  db_path = args.db_path

  dieIf(os.path.exists(db_path), "File '" + db_path + "' already exists.\n")

  db = sqlalchemy.create_engine('sqlite:///' + db_path)

  base.Base.metadata.create_all(db)

