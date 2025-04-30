# -*- coding: utf-8 -*-
__title__   = "SelectByUser"
__doc__     = """Version = 1.0
Date    = 15.06.2024
________________________________________________________________
Description:

-

________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================
# 📦 Create Default Dict Container
from collections import defaultdict
dict_elements_by_user = defaultdict(list)

#1️⃣ Get 3D Elements in The Project
elements = FilteredElementCollector(doc).WhereElementIsNotElementType().WhereElementIsViewIndependent().ToElements()

#2️⃣ Who Did This?
# elements = list(elements)[:30]
for elem in elements:
    wti = WorksharingUtils.GetWorksharingTooltipInfo(doc, elem.Id)
    changed_by = wti.LastChangedBy

    # owner      = wti.Owner
    # creator    = wti.Creator
    # print(owner, changed_by, creator)

    # 3️⃣ Sort Elements By User
    dict_elements_by_user[changed_by].append(elem)

# for k,v in dict_elements_by_user.items():
#     print('User: {} has modified {} Elements'.format(k, len(v) ))

#4️⃣ Select User
from pyrevit import forms
selected_user     = forms.SelectFromList.show(dict_elements_by_user.keys(), button_name='Select Item')
if not selected_user:
    forms.alert('No User Was Selected. Please Try Again.', exitscript=True)

selected_elements = dict_elements_by_user[selected_user]

# print('-*50')
# print('Selected {} Elements by {}'.format(len(selected_elements), selected_user))

#5️⃣ Modify User Selection
selected_el_ids      = [e.Id for e in selected_elements]
List_selected_el_ids = List[ElementId](selected_el_ids)
uidoc.Selection.SetElementIds(List_selected_el_ids)

# print('The Job Is Done! Congrats 🥳')
