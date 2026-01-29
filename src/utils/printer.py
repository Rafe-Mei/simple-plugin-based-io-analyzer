from models import models
from core import config
from pathlib import Path


from managers import project_manager as pm



# Print a divider.
def print_divider(length:int = 50):
    print("-" * length)




# Print the help text.
def print_help_text(help_text:models.HelpType):
    help_text_path = config.BASE_DIR / "resources" / "help text" / help_text.value
    content = help_text_path.read_text(encoding='utf-8')
    print("")
    print(content)


# Print all the projct folders.
def show_projects():
    header = ["ID", "Project Name"]
    print(f"{header[0]:<5} {header[1]}")
    project_dict = pm.get_project_dict()
    for i in project_dict.keys():
        pj_index = str(i) + "."
        pj_name = project_dict[i]
        print(f"{pj_index:<5} {pj_name}")




# Print the current project information.
def print_project_info():
    print("")

    header = ["Info","Detail"]
    print(f"{header[0]:<20} {header[1]}")
   
    titles = ["Project Name", "Units Dictionary"]
    print(f"{titles[0]:<20} {config.CURRENT_PROJECT_NAME}")
    print(f"{titles[1]:<20} {str(config.UNIT_NAMES_DICT)}")
    


# Print all units.
def show_units_list():
    print("\n[Units List]")
    header = ["ID","Unit Name"]
    print(f"{header[0]:<5} {header[1]}")
    for i in config.UNIT_NAMES_DICT:
        print(f"{i:<5} {config.UNIT_NAMES_DICT[i]}")

    

# Show all data in specified unit table.
def show_unit_content(unit_id:int):
    unit_df = config.UNIT_DF_DICT[unit_id]
    print(unit_df)


# Print all plugins in the plugins folder.
def show_plugins():
    header = ["ID", "Plugin Name"]
    print(f"{header[0]:<5} {header[1]}")
    for i in config.PLUGINS_DICT:
        print(f"{i:<5} {config.PLUGINS_DICT[i]}")



def show_plugin_info():
    print("")
    header = ["Info","Detail"]
    print(f"{header[0]:<20} {header[1]}")

    titles = ["Plugin Name", "Version", "Author", "Category"]
    print(f"{titles[0]:<20} {config.PLUGIN_INSTANCE.name}")
    print(f"{titles[1]:<20} {config.PLUGIN_INSTANCE.version}")
    print(f"{titles[2]:<20} {config.PLUGIN_INSTANCE.author}")
    print(f"{titles[3]:<20} {config.PLUGIN_INSTANCE.category}")
    


