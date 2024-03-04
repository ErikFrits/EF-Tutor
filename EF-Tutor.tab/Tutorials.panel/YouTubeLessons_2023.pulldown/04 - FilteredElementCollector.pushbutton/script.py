# -*- coding: utf-8 -*-
__title__ = "04 - Samples: FilteredElementCollector"
__helpurl__ = 'https://ko-fi.com/s/14b0b8e31c'
__doc__ = """This script is from YouTube Tutorial about FilteredElementCollector
You will learn how to use this class to get elements from your project. 
_____________________________________________________________________
Check out my E-Book on FilteredElementCollector and Filters on Ko_Fi page."""
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

import clr
clr.AddReference('System')
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application

active_view = doc.ActiveView
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

# GET SIMPLE ELEMENTS
all_rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
all_walls = FilteredElementCollector(doc).OfClass(Wall).WhereElementIsNotElementType().ToElements()
all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
all_windows = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()

# FILTER ELEMENTS
all_views   = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
all_legends = [view for view in all_views if view.ViewType == ViewType.Legend]

# GET ELEMENTS IN VIEW
all_furn_in_view = FilteredElementCollector(doc, active_view.Id)\
    .OfCategory(BuiltInCategory.OST_Furniture).WhereElementIsNotElementType().ToElements()

# COMBINE MULTIPLE CATEGORIES - SIMPLE
all_combined = list(all_rooms) + list(all_walls) + list(all_doors)
# print(all_combined)

# COMBINE MULTIPLE CATEGORIES - FILTERS
categories = List[BuiltInCategory]([BuiltInCategory.OST_Walls,
                                      BuiltInCategory.OST_Floors,
                                      BuiltInCategory.OST_Roofs,
                                      BuiltInCategory.OST_Ceilings])

custom_filter = ElementMulticategoryFilter(categories)
my_elements = FilteredElementCollector(doc).WherePasses(custom_filter).WhereElementIsElementType().ToElements()

# WORKSET
all_worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()