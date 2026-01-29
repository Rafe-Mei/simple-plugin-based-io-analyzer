import pandas as pd

from models import plugin_base
from core import config
from utils import printer




# 这个插件每个单元表示一个月的所有财务收支，组就表示全年的收支
# 下一个插件表示一个大类（如餐饮、日常支出、分期支出、收入）等，组表示一个月的支出。



HELP_TEXT = '''\\help: Show the help text.
\\info: Show the information of the analysis plugin.
\\q: Back to the main menu.

\\s: Select the analysis target.
\\a: Start to analyze.'''




class Plugin(plugin_base.AnalysisPlugin):
    # Basic information of the plugin.
    name = "Basic"
    version = "1.0.0"
    author = "Rafe Mei"
    category = "Default"
    

    def __init__(self):
        self.analysis_target_list = ["Single unit", "Unit vs unit (Compare)", "All units (Compare)", "Group"]
        self.analysis_target = None
        self.target_unit_id = None             

    
    
  
    # Build the command mapping dictionary.
    def build_command_dict(self):
        return {
            "\\help": self.print_help_text,
            "\\info": printer.show_plugin_info,

            "\\s": self.select_analysis_target,
            "\\a": self.analysis_router
        }




    # Show the help text.
    def print_help_text(self):
        print("\n[Analysis Plugin Commands]")
        print(HELP_TEXT)

    


    # Select an analysis target.
    def select_analysis_target(self):
        original_status = config.USER_CURRENT_STATUS
        config.switch_user_current_status("Target")

        while True:
            self.analysis_target = None
            self.target_unit_id = None
            
            printer.print_divider()
            print(f"{config.USER_CURRENT_STATUS} Analysis targets:")
            print("")
            for i, item in enumerate(self.analysis_target_list, start=1):
                print(f"{i}. {item}")

            print("")
            user_input = input(f"{config.USER_CURRENT_STATUS} Select an option: ")
            
            if user_input in ("1", "2", "3", "4"):
                index = int(user_input) - 1
                self.analysis_target = self.analysis_target_list[index]             # Set the analysis target in the plugin config.
                
                # Get the single unit's ID.
                if user_input == "1":
                    input_id = int(input(f"{config.USER_CURRENT_STATUS} Input the unit id: "))
                    if input_id not in config.UNIT_NAMES_DICT:
                        print("[Error] Wrong unit ID. Please check your input.")
                        continue
                    else:
                        self.target_unit_id = input_id
                
                # Get the units' ID tuple.
                if user_input == "2":
                    unit_A_id = int(input(f"{config.USER_CURRENT_STATUS} Input the unit A's id: "))
                    unit_B_id = int(input(f"{config.USER_CURRENT_STATUS} Input the unit B's id: "))
                    if unit_A_id not in config.UNIT_NAMES_DICT or unit_B_id not in config.UNIT_NAMES_DICT:
                        print("[Error] Wrong unit ID. Please check your input.")
                        continue
                    else:
                        self.target_unit_id = (unit_A_id, unit_B_id)

                print(f"{config.USER_CURRENT_STATUS} Selected successfully! The current analysis target is: {self.analysis_target} {self.target_unit_id}")
                break
            else:
                print("[Error] Invalid command!")
                continue

        config.switch_user_current_status(original_status, method=2)

    


    # The analysis router.
    def analysis_router(self):
        if self.analysis_target is not None:
            router_dict = {
                self.analysis_target_list[0]: lambda: self.analyze_single_unit(self.target_unit_id),
                self.analysis_target_list[1]: lambda: self.analyze_two_units_compare(self.target_unit_id[0], self.target_unit_id[1]),
                self.analysis_target_list[1]: self.analyze_all_units_compare,
                self.analysis_target_list[3]: self.analyze_group
            }
            router_dict[self.analysis_target]()         
        else:
            print("[Error] You havn't selected the analysis target!")





    # ------------------------------------ Write your analysis functions below. -------------------------------------- #



    # --------------------------------------------- Analyze single unit. --------------------------------------------- #



    def analyze_single_unit(self, unit_id:int):
        # Get the unit DataFrame.
        df_unit:pd.DataFrame = config.UNIT_DF_DICT[unit_id]
        df_in = df_unit[df_unit["io"] == "I"]
        df_out = df_unit[df_unit["io"] == "O"]
        

        inflow_dict ={
            "sum": df_in["amount"].sum(),
            "average": round(df_in["amount"].mean(), 2),
            "median": round(df_in["amount"].median(), 2),
            "max": self.get_max_record(df_in),
            "prop": self.get_category_proportion(df_in)
        }

        outflow_dict = {
            "sum": df_out["amount"].sum(),
            "average": round(df_out["amount"].mean(), 2),
            "median": round(df_out["amount"].median(), 2),
            "max": self.get_max_record(df_out),
            "prop": self.get_category_proportion(df_out)
        }          



        result_list = [
            ("Inflow", ""), 
            ("sum", inflow_dict["sum"]), ("average", inflow_dict["average"]), ("median", inflow_dict["median"]), ("max", inflow_dict["max"]), ("prop", inflow_dict["prop"]),
            ("", ""), 
            ("Outflow", ""),
            ("sum", outflow_dict["sum"]), ("average", outflow_dict["average"]), ("median", outflow_dict["median"]), ("max", outflow_dict["max"]), ("prop", outflow_dict["prop"]),
        ]

        self.output_result(result_list)




    
    # Find the max IO record.
    def get_max_record(self, df:pd.DataFrame) -> str:
        if df.empty:
            return None
    
        row = df.loc[df["amount"].idxmax()]
        return f"{row["amount"]}  {row["category"]}  {row["subcategory"]}  {row["item"]}"
    


    # Calculate every category's proportion of total amount.
    def get_category_proportion(self, df:pd.DataFrame):
        category_total_df = df.groupby('category')['amount'].sum().reset_index()
        total_amount = df["amount"].sum()

        result_dict = {}

        for index, row in category_total_df.iterrows():
            category_amount = row["amount"]
            proportion = category_amount / total_amount

            proportion_str = f"{proportion*100:.1f}%"
            result_dict[row["category"]] = proportion_str
        
        return result_dict




    # ----------------------------------------- Analyze two units (Compare). ------------------------------------------ #


    def analyze_two_units_compare(self, unit_A_id:int, unit_B_id:int):
        # Get the unit A and unit B's DataFrames.
        df_unit_A:pd.DataFrame = config.UNIT_DF_DICT[unit_A_id]
        df_unit_B:pd.DataFrame = config.UNIT_DF_DICT[unit_B_id]


    # ----------------------------------------- Analyze two units (Compare). ------------------------------------------ #

    def analyze_all_units_compare(self):
        pass


    # ----------------------------------------------- Analyze one gruop ------------------------------------------------ #

    def analyze_group(self):
        df_group = config.GROUP_DF





    
