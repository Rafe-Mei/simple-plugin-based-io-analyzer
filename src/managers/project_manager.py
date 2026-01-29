from pathlib import Path

from core import config
from utils import csv_handler as ch





# Find all the project folders in the data folder.
def get_project_dict():
    data_folder_path = config.DATA_PATH
    project_list = []

    for p in data_folder_path.iterdir():
        if p.is_dir() and p.name != "OUTPUT":
            project_list.append(p.name)

    sorted_project_list = sorted(project_list)
    
    project_dict = {}
    for i in range (1, len(sorted_project_list)+1):
        project_dict[i] = sorted_project_list[i-1]

    return project_dict







# Load the specified project by its id.
def load_project_by_id(project_id:int):
    project_dict = get_project_dict()

    if project_id not in project_dict.keys():
        raise ValueError("Incorrect project id! Please check your input.")
    
    print(f"{config.USER_CURRENT_STATUS} Loading project...")
    
    pj_name = project_dict[project_id]

    # Set the current project info in config.py
    config.CURRENT_PROJECT_NAME = pj_name
    config.CURRENT_PROJECT_PATH = config.DATA_PATH / pj_name

    ch.register_units_dict()        # Register the units dictionary in config.py
    ch.all_units_to_dfs()
    ch.dfs_to_group()








# Check if user has loaded a project.
def check_if_project_plugin_loaded():
    if config.CURRENT_PROJECT_NAME is None or config.PLUGIN_INSTANCE is None:
        return False
    else:
        return True

