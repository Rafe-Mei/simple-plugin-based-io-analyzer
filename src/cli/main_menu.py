from core import config
from models import models

from managers import project_manager as pm
from managers import plugin_manager as plm
from utils import printer




# The start menu.
def main_menu():
    COMMANDS_DICT = build_commands_dict()

    while True:
        if config.USER_CURRENT_STATUS is None:
            config.switch_user_current_status("Main Menu")

        printer.print_divider()
        user_input = input(f"{config.USER_CURRENT_STATUS} Command: ")

        if user_input == "\\q":             # Quit the program.
            break
        
        elif user_input in COMMANDS_DICT:
            COMMANDS_DICT[user_input]()      
  
        else:
            print(f"[Error] Invalid command. You can input \\help to see the help text.")






# Build the commands dictionary for the main menu.
def build_commands_dict():
    COMMANDS_DICT = {
    "\\help": show_main_menu_help,
    "\\o": open_project_menu,
    "\\info": printer.print_project_info,
    "\\unit": show_units_and_content,
    "\\l": load_plugin_menu,
    "\\a": enter_analysis_menu
}
    return COMMANDS_DICT






# User can open a project in this menu.
def open_project_menu():
    original_status = config.USER_CURRENT_STATUS
    config.switch_user_current_status("Project")
    
    # Show the project list.
    print("")
    printer.show_projects()

    # Input the project id, then load the specified project.
    print("")
    try:
        id_input = int(input(f"{config.USER_CURRENT_STATUS} Input project ID to load: "))
        pm.load_project_by_id(id_input)
        print(f"{config.USER_CURRENT_STATUS} Load successfully! Current project Name: {config.CURRENT_PROJECT_NAME}")
        config.switch_user_current_status(config.CURRENT_PROJECT_NAME)
    except Exception as e:
        print(f"[Error] {e}")
        config.switch_user_current_status(original_status, method=2)
    
    





# Show all units in a list, and user can input id to check the table content.
def show_units_and_content():
    if config.CURRENT_PROJECT_NAME is not None:
        config.switch_user_current_status("View")
        printer.show_units_list()
        
        while True:
            printer.print_divider()
            print(f"{config.USER_CURRENT_STATUS} Now you can input Unit ID to view its content, or input \\q to quit.")
            
            user_input:str = input(f"{config.USER_CURRENT_STATUS} Command: ")
            if user_input == "\\q":
                config.switch_user_current_status(config.CURRENT_PROJECT_NAME)
                break
    
            try:
                id = int(user_input)
                print("")
                print(f"Unit_{id}: {config.UNIT_NAMES_DICT[id]}")
                printer.show_unit_content(id)
            except:
                print("[Error] Invalid command! Please check your input.")
    else:
        print("[Error] No project loaded! Please open a project first.")







# User can load a plugin here.
def load_plugin_menu():
    original_status = config.USER_CURRENT_STATUS
    config.switch_user_current_status("Plugin")

    plm.register_scanned_plugins()
    print("")
    printer.show_plugins()
    
    print("")
    user_input = input(f"{config.USER_CURRENT_STATUS} Input plugin ID to load: ")
    
    try:
        if int(user_input) in config.PLUGINS_DICT:
            plm.register_plugin_instance(int(user_input))
            print(f"{config.USER_CURRENT_STATUS} Loaded successfully! Current plugin name: {config.PLUGIN_INSTANCE.name}")
        else:
            raise ValueError("Invalid plugin id.")
    except Exception as e:
        print(f"[Error] Falied to load the plugin: {e}")
    
    config.switch_user_current_status(original_status, method=2)






# Initialize the DataFrames, and then enter the analysis menu.
def enter_analysis_menu():
    if pm.check_if_project_plugin_loaded():
        config.switch_user_current_status("Analysis")
        config.PLUGIN_INSTANCE.analysis_menu()                  # Enter the analysis menu.
        config.switch_user_current_status(config.CURRENT_PROJECT_NAME)          # Change the current status in config if user back to main menu.
    else:
        print("[Error] You haven't loaded the project or plugin.")





# Print the help text of main menu.
def show_main_menu_help():
    printer.print_help_text(models.HelpType.MAIN_MENU_HELP)