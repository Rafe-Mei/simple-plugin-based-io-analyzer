from enum import Enum

from core import config


class HelpType(Enum):
    MAIN_MENU_HELP = "main menu help.txt"
    ANALYZE_MODE_HELP = "analyze mode help.txt"



class UnitRow:
    def __init__(self, category, subcategory, item, io,  amount):
        self.category = category
        self.subcategory = subcategory
        self.item = item
        self.io = io
        self.amount = amount