# -*- coding: utf-8 -*-
__title__ = '4 - pyRevit Linkify'

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
from Autodesk.Revit.DB import *
from pyrevit import script

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#--------------------------------------------------
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document  #type: Document
output = script.get_output()
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝


# 1️⃣ Linkify Single - Walls
all_walls = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(Wall).ToElements()

for wall in all_walls:
    linkify_wall = output.linkify(wall.Id, wall.Name)
    print(linkify_wall)
#--------------------------------------------------

#2️⃣ Linkify Multiple - Walls
all_walls     = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(Wall).ToElements()
wall_ids      = [wall.Id for wall in all_walls]
linkify_walls = output.linkify(wall_ids, 'Walls {}'.format(len(wall_ids)))
print(linkify_walls)
#--------------------------------------------------

#3️⃣ Limit ~100-150 elements
all_walls     = FilteredElementCollector(doc).OfClass(Wall).ToElements()
wall_ids      = [wall.Id for wall in all_walls]
linkify_walls = output.linkify(wall_ids, 'Walls {}'.format(len(wall_ids)))
print('Here are all the walls in the project: {}'.format(linkify_walls))
#------------------------------------------------

# 4️⃣ Linkify - Views
# all_views_and_vt = FilteredElementCollector(doc).OfClass(ViewPlan).ToElements()
# all_views        = [view for view in all_views_and_vt if not view.IsTemplate]
#
# for view in all_views:
#     linkify_view = output.linkify(view.Id, 'View: {}'.format(view.Name))
#     print(linkify_view)
# -----------------------------------------------

#5️⃣ Bonus Example: Analyze Warnings
def get_sorted_warnings():
    """Function to get All Warnings in the project and sort them by their description
    :return: dict of warnings {warn_description : list_of_warnings}"""
    from collections import defaultdict

    dict_all_warnings = defaultdict(list)
    for w in doc.GetWarnings():
        description = w.GetDescriptionText()
        dict_all_warnings[description].append(w)
    return dict_all_warnings

# Get + Sort Warnings
dict_all_warnings = get_sorted_warnings()

for descr, list_warnings in dict_all_warnings.items():
    table_data = []

    for warn in list_warnings:

        # print(warn)
        element_ids      = list(warn.GetFailingElements()) + list(warn.GetAdditionalElements())
        last_modified_by = {WorksharingUtils.GetWorksharingTooltipInfo(doc, el_id).LastChangedBy for el_id in element_ids}
        last_modified_by = ', '.join(last_modified_by)

        # Linkify
        title = 'Select'
        warn_linkify = output.linkify(element_ids, title)

        # Create a Row of Data
        row = [descr, last_modified_by, str(len(element_ids)), warn_linkify]
        table_data.append(row)
    output.print_table(table_data=table_data,
                       title  =descr,
                       columns=['Warning Description', 'Last Modified By:', 'Elements', 'Linkify'],
                       formats=['**{}**', '*{}*', '', ''])


