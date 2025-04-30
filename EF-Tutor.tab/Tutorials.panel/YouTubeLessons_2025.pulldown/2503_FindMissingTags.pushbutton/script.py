# -*- coding: utf-8 -*-
__title__   = "Find Missing DoorTags"

#⬇️ Imports
from Autodesk.Revit.DB import *

#📦 Variables
uidoc    = __revit__.ActiveUIDocument
doc      = __revit__.ActiveUIDocument.Document #type: Document
active_view = doc.ActiveView

# 🎯 MAIN
#
# #1️⃣ - Get Doors and DoorTags in View
# all_doors_in_view     = FilteredElementCollector(doc, active_view.Id)\
#                                                 .OfCategory(BuiltInCategory.OST_Doors)\
#                                                 .WhereElementIsNotElementType()\
#                                                 .ToElements()
# all_door_tags_in_view = FilteredElementCollector(doc, active_view.Id)\
#                                                 .OfCategory(BuiltInCategory.OST_DoorTags)\
#                                                 .WhereElementIsNotElementType()\
#                                                 .ToElements()
#
# # print(len(all_doors_in_view))
# # print(len(all_door_tags_in_view))
#
#
# #2️⃣ - Find Untagged Doors
# tagged_doors = []
# for tag in all_door_tags_in_view:
#     tag_elements = tag.GetTaggedLocalElements()
#     tagged_doors += tag_elements
#
# tagged_door_ids    = [d.Id for d in tagged_doors]
# untagged_doors_ids = [d.Id for d in all_doors_in_view if d.Id not in tagged_door_ids]
#
#
# #3️⃣ Select Untagged Doors
# import clr
# clr.AddReference('System')
# from System.Collections.Generic import List
#
# List_untagged_door_ids = List[ElementId](untagged_doors_ids)
# uidoc.Selection.SetElementIds(List_untagged_door_ids)



# 4️⃣ Create a reusable function
def find_untagged_door_ids(view):
    #1️⃣ - Get Doors and DoorTags in View
    all_doors_in_view     = FilteredElementCollector(doc, view.Id)\
                                                    .OfCategory(BuiltInCategory.OST_Doors)\
                                                    .WhereElementIsNotElementType()\
                                                    .ToElements()
    all_door_tags_in_view = FilteredElementCollector(doc, view.Id)\
                                                    .OfCategory(BuiltInCategory.OST_DoorTags)\
                                                    .WhereElementIsNotElementType()\
                                                    .ToElements()

    #2️⃣ - Find Untagged Doors
    tagged_doors = []
    for tag in all_door_tags_in_view:
        tag_elements = tag.GetTaggedLocalElements()
        tagged_doors += tag_elements

    tagged_door_ids    = [d.Id for d in tagged_doors]
    untagged_doors_ids = [d.Id for d in all_doors_in_view if d.Id not in tagged_door_ids]

    return untagged_doors_ids



#5️⃣ Select Views
from pyrevit import forms
sel_views = forms.select_views()
# for v in sel_views:
#     print(v.Name)

#6️⃣ Find Missing DoorTags
from pyrevit import script
output = script.get_output()
output.print_md("# Missing Door Tags Report:")
output.print_md("---")

for view in sel_views:
    untagged_door_ids = find_untagged_door_ids(view)
    linkify_view      = output.linkify(view.Id, view.Name)

    if untagged_door_ids:
        output.print_md('### View: {}'.format(linkify_view))

        for door_id in untagged_door_ids:
            door         = doc.GetElement(door_id)
            linkify_door = output.linkify(door_id, door.Name)
            print('Missing Tag Door: {}'.format(linkify_door))
    else:
        output.print_md('### View: {} has no doors with missing tags.'.format(linkify_view))

    output.print_md("---")
