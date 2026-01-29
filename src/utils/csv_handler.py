from pathlib import Path
import csv
import pandas as pd


from core import config
from models import models



# Get the project's CSV file names as a dictionary.
# For instance, {'001': 'Revenue', '002': 'Expenses'}
def get_project_csv_dict():
    if config.CURRENT_PROJECT_PATH is None:
        raise ValueError("No project is loaded! Please load a project first.")
    project_path = config.CURRENT_PROJECT_PATH
    
    csv_files_list = [file.name for file in Path(project_path).glob("*.csv")]

    csv_files_dict = {}
    for f_name in csv_files_list:
        id = int(f_name.split("_")[0])
        name = str(f_name.split("_")[1]).replace(".csv", "")
        csv_files_dict[id] = name

    return csv_files_dict 



# Register the units dictionary in config.py.
def register_units_dict():
    try:
        config.UNIT_NAMES_DICT = get_project_csv_dict()
    except ValueError as e:
        print(f"[Error] {e}")








# Convert one csv file to a DataFrame.
def csv_to_unit_df(unit_id:int):
    file_name = f"{unit_id}_{config.UNIT_NAMES_DICT[unit_id]}.csv"
    csv_file_path = config.CURRENT_PROJECT_PATH / file_name
    
    df = pd.read_csv(csv_file_path, encoding='utf-8-sig')

    return df



# Put all unit DataFrames in one group dict, and register the dict to config.
def all_units_to_dfs():
    dfs_dict = {}
    for i in config.UNIT_NAMES_DICT:
        new_df:pd.DataFrame = csv_to_unit_df(i)
        dfs_dict[i] = new_df
    
    config.UNIT_DF_DICT = dfs_dict



# Combine all DataFrames into a big one, and register it to config.
def dfs_to_group():
    dfs_dict = config.UNIT_DF_DICT
    group_df =  pd.concat(dfs_dict.values(), ignore_index=True)
    
    config.GROUP_DF = group_df

