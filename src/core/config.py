from pathlib import Path
from models import models
import pandas


BASE_DIR = Path(__file__).parent.parent.parent         # Folder: Group Financial IO Analyzer

# Important Paths.
DATA_PATH = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database.sqlite3"
PLUGINS_DIR = BASE_DIR / "src" / "plugins"





# User's current status.
USER_CURRENT_STATUS = None

# This function switches the user's current status.
def switch_user_current_status(status:str, method:int=1):
    global USER_CURRENT_STATUS
    if method == 1:
        USER_CURRENT_STATUS = f"[{status}]"
    elif method == 2:
        USER_CURRENT_STATUS = status





# User's project.
CURRENT_PROJECT_NAME = None
CURRENT_PROJECT_PATH = None


# This is units dictionary extracted from the CSV file names.
UNIT_NAMES_DICT = {}





# Groups' DataFrames.
UNIT_DF_DICT:dict = None
GROUP_DF:pandas.DataFrame = None





# Analysis plugins.
PLUGINS_DICT = {}
PLUGIN_INSTANCE = None
