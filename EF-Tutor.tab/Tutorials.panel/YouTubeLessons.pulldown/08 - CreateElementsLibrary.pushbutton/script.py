# -*- coding: utf-8 -*-
__title__   = "08 - Create Library of Elements"
__doc__ = """Date    = 22.10.2022
_____________________________________________________________________
Description:
Script from a video Tutorial for my Ko-Fi and Patreon supporters.
_____________________________________________________________________
Author:  Erik Frits"""
__context__ = 'active-floor-plan'

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#====================================================================================================
from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#====================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view  = doc.ActiveView
active_level = doc.ActiveView.GenLevel

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
#====================================================================================================
def create_text(origin, text_type):
    """Function to create TextNote at the given location.
    TextType Name is going to be used as a Text."""
    text         = text_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()

    # CREATE TEXT NOTE
    txt = TextNote.Create(doc, active_view.Id, origin, text, text_type.Id)
    return txt

def create_wall(origin, wall_type):
    """Function to create a Wall at the given location."""
    pt_start = origin
    pt_end   = XYZ(origin.X + 2, origin.Y, origin.Z)
    curve    = Line.CreateBound(pt_start, pt_end)

    H = 10
    O = 0
    flip  = False
    struc = False

    wall = Wall.Create(doc, curve, wall_type.Id, active_level.Id, H, O, flip, struc)
    return wall


def create_floor(origin, floor_type):
    """Function to create a Floor at the given location."""
    # POINTS
    pt_0 = origin
    pt_1 = XYZ(origin.X+1 , origin.Y   , origin.Z)
    pt_2 = XYZ(origin.X+1 , origin.Y+1 , origin.Z)
    pt_3 = XYZ(origin.X   , origin.Y+1 , origin.Z)

    # LINES
    l_0 = Line.CreateBound(pt_0, pt_1)
    l_1 = Line.CreateBound(pt_1, pt_2)
    l_2 = Line.CreateBound(pt_2, pt_3)
    l_3 = Line.CreateBound(pt_3, pt_0)

    # BOUNDARY
    boundary = CurveArray()
    boundary.Append(l_0)
    boundary.Append(l_1)
    boundary.Append(l_2)
    boundary.Append(l_3)

    # CREATE FLOOR
    new_floor = doc.Create.NewFloor(boundary, floor_type, active_level, False)
    return new_floor

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#====================================================================================================
# Get Types
all_walls_types  = FilteredElementCollector(doc).OfClass(WallType).ToElements()
all_floors_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).OfClass(FloorType).ToElements()
all_text_types   = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()

#🔵 ORIGIN
X = 0
Y = 0
Z = 0


#🔓 Transaction - Start
t = Transaction(doc, __title__)
t.Start()


#✅ Create TextTypes
for txt_type in all_text_types:
    origin = XYZ(X,Y,Z)
    create_text(origin, txt_type)
    Y -= 2

X += 15
Y = 0

#✅ Create WallType
for wall_type in all_walls_types:
    origin = XYZ(X,Y,Z)
    create_wall(origin, wall_type)
    Y -= 2

X += 15
Y = 0

#✅ Create FloorType
for floor_type in all_floors_types:
    origin = XYZ(X,Y,Z)
    create_floor(origin, floor_type)
    Y -= 2


#🔒 Transaction - Commit
t.Commit()
