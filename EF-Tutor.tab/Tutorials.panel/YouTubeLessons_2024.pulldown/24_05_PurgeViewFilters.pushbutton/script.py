# -*- coding: utf-8 -*-
__title__ = "5 - Purge Unused View Filters"
__doc__ = """Version = 1.0
Date    = 24.06.2024
_____________________________________________________________________
Description:
Purge Unused View Filters from your Revit Project.
_____________________________________________________________________
How-To:
- Click the Button
- Select unused View Filters to purge
_____________________________________________________________________
Last update:
- [24.06.2024] - V1.0 RELEASE
_____________________________________________________________________
Author: Erik Frits from LearnRevitAPI.com"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import forms

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc    = __revit__.ActiveUIDocument.Document
uidoc  = __revit__.ActiveUIDocument

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
# 1️⃣ Get Views and Filters
# all_filter_ids     = FilteredElementCollector(doc).OfClass(FilterElement).ToElementIds() #Parameter + Selection
# all_sel_filter_ids = FilteredElementCollector(doc).OfClass(SelectionFilterElement).ToElementIds()
all_param_filter_ids = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElementIds()
all_views_and_vt     = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()


#2️⃣ Find Used ViewFilters
used_filter_ids = []

for view in all_views_and_vt:
    view_filter_ids = view.GetFilters()

    for view_filter_id in view_filter_ids:
        if view_filter_id not in used_filter_ids:
            used_filter_ids.append(view_filter_id)

#3️⃣ Get Unused ViewFilters
unused_filter_ids = set(all_param_filter_ids) - set(used_filter_ids)
unused_filters    = [doc.GetElement(f_id) for f_id in unused_filter_ids]

#✅ Check if Unused Filters in Project
if not unused_filters:
    forms.alert('There are no Unused View Filters in the project. Please try again',title=__title__, exitscript=True)

#👉 Select View Filters to Delete
filters_to_del = forms.SelectFromList.show(unused_filters,
                                multiselect=True,
                                name_attr='Name',
                                button_name='Select Unused View Filters To Delete.')


#✅ Check Selection
if not filters_to_del:
    forms.alert('No Unused View Filters were selected. Please try again',title=__title__, exitscript=True)


with Transaction(doc, 'Purge Unused ViewFilters') as t:
    t.Start()  #🔓

    for fil in filters_to_del:
        try:
            f_name = fil.Name
            doc.Delete(fil.Id)
            print('✔️ Deleted ViewFilter: {}'.format(f_name))
        except Exception as e:
            print("✖️ Couldn't Delete View Filter: {}".format(f_name))
            print('----- Error Message: {}'.format(e))

    t.Commit() #🔒

