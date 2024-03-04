# -*- coding: utf-8 -*-
__title__ = "07 - Furniture Rooms"
__doc__ = """Date    = 19.03.2023
Get all Furniture and Plumbing elements and write Room's name 
if available to a comment Parameter.
_____________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
from Autodesk.Revit.DB  import *
from Autodesk.Revit.UI  import UIDocument, UIApplication

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
uidoc        = __revit__.ActiveUIDocument           #type: UIDocument
doc          = __revit__.ActiveUIDocument.Document  #type: Document
app          = __revit__.Application                #type: UIApplication

all_phases  = list(doc.Phases)
phase       = all_phases[-1]

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

#1️⃣ Get Elements
all_furniture = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Furniture).WhereElementIsNotElementType().ToElements()
all_f_systems = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_FurnitureSystems).WhereElementIsNotElementType().ToElements()
all_plumbing  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PlumbingFixtures).WhereElementIsNotElementType().ToElements()

all_elements = list(all_furniture) + list(all_f_systems) + list(all_plumbing)

# 🔓 Start Transaction
t = Transaction(doc, __title__)
t.Start()

#2️⃣ Iterate and get Rooms
for el in all_elements:
    room = el.Room[phase]
    # print(room)
    if room:
        #3️⃣ Read Room Name and Number
        # room_name   = Element.Name.GetValue(room)
        room_name   = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
        room_number = room.Number

        #4️⃣ Get Element Parameters
        p_room_name   = el.LookupParameter('Room Name')
        p_room_number = el.LookupParameter('Room Number')

        #5️⃣ Write Room Name and Number to Parameters
        if p_room_name:
            p_room_name.Set(room_name)

        if p_room_number:
            p_room_number.Set(room_number)

t.Commit()

