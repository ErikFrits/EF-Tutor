# -*- coding: utf-8 -*-
__title__ = "01 - Add Levels Elevation"                  # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 20.04.2022
_____________________________________________________________________
Description:

This tool will add/update your level name to have its elevation.
_____________________________________________________________________
How-to:

-> Click on the button
-> Change Settings(optional)
-> Rename Levels
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
_____________________________________________________________________
Author: Erik Frits"""                                                      # Button Description shown in Revit UI

#EXTRA:
__author__        = "Erik Frits"                                           # Script's Author
__helpurl__       = "https://www.youtube.com/watch?v=YhL_iOKH-1M&t=626s"   # Link that can be opened with F1 when hovered over the tool in Revit UI.
# __highlight__     = "new"                                                # It will have an orange dot + Description in Revit UI
__min_revit_ver__ = 2019                                                   # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
__max_revit_ver   = 2022                                                   # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
# __context__     = ['Walls', 'Floors', 'Roofs']                           # Make your button available only when certain categories are selected

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
import os
from Autodesk.Revit.DB import *                                     # Import everything from DB (Very good for beginners and during development)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector # or Import only used classes.

# pyRevit
from pyrevit import revit, forms

# Custom Imports
from Snippets._selection import get_selected_elements
from Snippets._convert   import convert_internal_to_m

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List                         # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires sometimes.

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc     = __revit__.ActiveUIDocument.Document                       # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc   = __revit__.ActiveUIDocument                                # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI(user interface).
app     = __revit__.Application                                     # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)                             # Absolute path to the folder where this current script is located. Used
# from pyrevit.revit import uidoc, doc, app                         # Alternative import option

# Global Settings
symbol_start = "【"
symbol_end   = "】"
mode         = 'add'                # 'add'/'remove'
position     = 'prefix'             # 'prefix'/'suffix'

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
#==================================================

# Place local functions here. If you might use any functions in other scripts, consider placing it in the lib folder.

def get_text_in_brackets(text, symbol_start, symbol_end):
    #type:(str,str,str) -> str
    """Function to get content between 2 symbols
    :param text:            Initial Text
    :param symbol_start:    Start Symbol
    :param symbol_end:      End Symbol
    :return:                Text between 2 symbols, if found.
    e.g. get_text_in_brackets('This is [not] very important message.', '[', ']') -> 'not'"""
    if symbol_start in text and symbol_end in text:
        start = text.find(symbol_start) + len(symbol_start)
        stop  = text.find(symbol_end)
        return text[start:stop]
    return ""

# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ CLASSES
#==================================================

# Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
if __name__ == '__main__':
    # Get all Levels
    all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements() # FilteredElementCollector is the common class for getting specific elements from Revit.

    # DO NOT place Transaction inside of your loops! It will drastically reduce perfomance of your script.
    t = Transaction(doc, __title__)         # Transactions are context-like objects that guard any changes made to a Revit model. You need to use t.Start() and t.Commit() to make changes to a Project.
    t.Start()                               # <- Transaction Start

    for lvl in all_levels:
        # Get Levels Elevations + convert to meters
        lvl_elevation       = lvl.Elevation
        lvl_elevation_m     = round(convert_internal_to_m(lvl.Elevation), 2)
        lvl_elevation_m_str = "+" + str(lvl_elevation_m) if lvl.Elevation > 0 else str(lvl_elevation_m)

        # Prepare New Name - ELEVATION EXISTS (update)
        if symbol_start in lvl.Name and symbol_end in lvl.Name:
            current_value   = get_text_in_brackets(lvl.Name, symbol_start, symbol_end)
            new_name        = lvl.Name.replace(current_value, lvl_elevation_m_str)
            #TODO Homework: Add an option to remove Elevation from levels name.

        # Prepare New Name - ELEVATION DOES NOT EXIST (new)
        else:
            elevation_value = symbol_start + lvl_elevation_m_str + symbol_end
            new_name = lvl.Name + elevation_value
            #TODO Homework: Different Elevation Position = 'Prefix'/'Suffix'

        # Add/Update Levels Elevation
        try:
            # Ensure that new_name is different that current.
            if lvl.Name != new_name:
                current_name = lvl.Name
                lvl.Name     = new_name
                # REPORT: if Level has changed.
                print('Renamed: {} -> {}'.format(current_name, new_name))
        except:
            print("Could not change Level's name...")

    t.Commit()                              # <- Transaction End

    # Notify user that script is complete.
    print('-'*50)
    print('Script is finished. Type keyboard emoji in the comments if you managed to follow it until here -> ⌨')