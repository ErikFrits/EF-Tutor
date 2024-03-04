# -*- coding: utf-8 -*-
__title__ = "11 - Get Default Element Types"
__doc__ = """Version = 1.0
Date    = 15.01.2024
_____________________________________________________________________
Description:
Learn How to get Default Element Types with Revit API.

Happy Coding!
_____________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc   = __revit__.ActiveUIDocument.Document     #type: Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

#1. Get Types of Native Families (GetDefaultElementTypeId )
wall_type_id      = doc.GetDefaultElementTypeId(ElementTypeGroup.WallType)
floor_type_id     = doc.GetDefaultElementTypeId(ElementTypeGroup.FloorType)
view_plan_type_id = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeFloorPlan)
region_type_id    = doc.GetDefaultElementTypeId(ElementTypeGroup.FilledRegionType)

# Convert to Elements
wall_type      = doc.GetElement(wall_type_id)
floor_type     = doc.GetElement(floor_type_id)
view_plan_type = doc.GetElement(view_plan_type_id)
region_type    = doc.GetElement(region_type_id)

# Display Results
print(Element.Name.GetValue(wall_type))
print(Element.Name.GetValue(floor_type))
print(Element.Name.GetValue(view_plan_type))
print(Element.Name.GetValue(region_type))


#2. Get Types of Loaded Families (GetDefaultFamilyTypeId )
door_type_id      = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_Doors))
win_type_id       = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_Windows))
gen_model_type_id = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_GenericModel))

door_type      = doc.GetElement(door_type_id)
win_type       = doc.GetElement(win_type_id)
gen_model_type = doc.GetElement(gen_model_type_id)

# Display Results
print(Element.Name.GetValue(door_type))
print(Element.Name.GetValue(win_type))
print(Element.Name.GetValue(gen_model_type))