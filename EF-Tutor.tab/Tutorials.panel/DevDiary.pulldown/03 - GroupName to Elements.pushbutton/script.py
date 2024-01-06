# -*- coding: utf-8 -*-
__title__ = "03 - GroupName to Elements"
__doc__ = """This script is from Dev Diary video that I 
posted on Patreon. I will show you how to :
- Get Groups
- Get Elements in Groups
- Get Group Name
- Write Groupname to one of parameters.

You can support my channel on:
www.patreon.com/ErikFrits"""
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application

OUTPUT_PARAM = 'GroupName'
CATEGORIES = [BuiltInCategory.OST_Walls, BuiltInCategory.OST_Floors]

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

# GET ALL GROUPS + FILTER
all_groups     = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSModelGroups).WhereElementIsNotElementType().ToElements()
all_whg_groups = [g for g in all_groups if 'WHG' in g.Name] # List Comprehension to filter Apartment groups.

with Transaction(doc, __doc__) as t:
    t.Start()

    # CLEAN PARAMETERS
    all_walls  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
    all_floors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
    all_doors  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
    clean_elements = list(all_walls) + list(all_floors) + list(all_doors)

    for el in clean_elements:
        el_param = el.LookupParameter(OUTPUT_PARAM)
        el_param.Set('')



    for g in all_whg_groups:
        # GET GROUP MEMBERS
        member_ids = g.GetMemberIds()
        members    = [doc.GetElement(id) for id in member_ids]

        # FILTER MEMBERS CATEGORIES
        for el in members:
            try:
                if el.Category.Name not in CATEGORIES:
                    continue
            except:
                continue

            # SET GROUP NAME
            el_param = el.LookupParameter(OUTPUT_PARAM)
            el_param.Set(g.Name)

        # break

    t.Commit()


