from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from core import config
from utils import printer


class AnalysisPlugin(ABC):
    # Basic information of the plugin.
    name:str
    version:str
    author:str
    category:str



    @abstractmethod
    def build_command_dict(self) -> dict:
        """Return command -> callable mapping"""
        pass


    @abstractmethod
    def select_analysis_target(self):
        pass




    # Show the analysis menu.
    def analysis_menu(self):
        commands_dict = self.build_command_dict()

        while True:
            printer.print_divider()

            user_input = input(f"{config.USER_CURRENT_STATUS} Command: ")

            if user_input == "\\q":
                break

            elif user_input in commands_dict:
                commands_dict[user_input]()                 # Excute the command function.
            
            else:
                print("[Error] Invalid command. You can input \\help to see the help text.")



    # Print or save the analysis results.
    def output_result(self, result_list:list, title_length:int=12):
        while True:
            original_status = config.USER_CURRENT_STATUS
            config.switch_user_current_status("Output")

            print(f"{config.USER_CURRENT_STATUS} Choose a output method:")
            print("1. Print   2. Save to txt   0. Cancel")
            
            header = ["Title", "Value"]

            print("")
            user_input = input(f"{config.USER_CURRENT_STATUS} Command: ")
            if user_input == "0":
                config.switch_user_current_status(original_status, method=2)
                break

            elif user_input == "1":
                print(f"{header[0]:<{title_length}}{header[1]}")
                for title, value in result_list:
                    print(f"{title:<{title_length}}{value}")
                config.switch_user_current_status(original_status, method=2)
                break
            
            elif user_input == "2":
                now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_name = f"Analysis Result [{now_str}].txt"
                txt_path = config.BASE_DIR / "output" / file_name

                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(f"{header[0]:<{title_length}}{header[1]}" + "\n\n")
                    for title, value in result_list:
                        f.write(f"{title:<{title_length}}{value}" + "\n")
                        
                print(f"{config.USER_CURRENT_STATUS} Analysis result has been saved to output folder successfully!")
                config.switch_user_current_status(original_status, method=2)
                break

            else:
                print("[Error] Invalid command! Please retry.")



            
