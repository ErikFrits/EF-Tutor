# -*- coding: utf-8 -*-
__title__   = "04 - Center Room Tags"
__author__  = "Erik Frits"
__version__ = "Version 1.0"
__doc__ = """Version = 1.0
Date    = 03.09.2022
_____________________________________________________________________
Description:
WIP:
Move your existing tags to the center of the room, 
together with reference of your Room.
_____________________________________________________________________
How-to:
-> Click on Button
_____________________________________________________________________
Author:  Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# ELEMENTS
all_room_tags = FilteredElementCollector(doc, doc.ActiveView.Id)\
    .OfCategory(BuiltInCategory.OST_RoomTags).WhereElementIsNotElementType().ToElements()

# CONTROLS
step = 2 # INTERNAL UNITS IN FEET


def move_room_and_tag(tag, room, new_pt):
    """Function to move both Room and Tag Locations, if they are not part of the group.
    :param tag:     Room Tag
    :param room:    Room
    :param new_pt:  XYZ Point."""
    if room.GroupId == ElementId(-1): #ElementId(-1) means None
        room.Location.Point = new_pt

    if tag.GroupId == ElementId(-1):
        tag.Location.Point = new_pt

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================

with Transaction(doc, __title__) as t:
    t.Start()


    for tag in all_room_tags:
        # ROOM DATA
        room = tag.Room
        room_bb = room.get_BoundingBox(doc.ActiveView)
        room_center = (room_bb.Min + room_bb.Max) / 2

        # MOVE TO CENTER (if possible)
        if room.IsPointInRoom(room_center):
            move_room_and_tag(tag, room, room_center)

        # FIND ANOTHER LOCATION
        else:
            room_boundaries = room.GetBoundarySegments(SpatialElementBoundaryOptions())
            room_segments   = room_boundaries[0]

            # Get Longest Segment
            length = 0
            longest_curve = None

            for seg in room_segments:
                curve = seg.GetCurve()
                if curve.Length > length:
                    longest_curve = curve
                    length = curve.Length

            # Get middle point on Curve
            pt_start = longest_curve.GetEndPoint(0)
            pt_end   = longest_curve.GetEndPoint(1)
            pt_mid   = (pt_start + pt_end) / 2

            pt_up    = XYZ(pt_mid.X       , pt_mid.Y +step , pt_mid.Z)
            pt_down  = XYZ(pt_mid.X       , pt_mid.Y -step , pt_mid.Z)
            pt_right = XYZ(pt_mid.X +step , pt_mid.Y       , pt_mid.Z)
            pt_left  = XYZ(pt_mid.X -step , pt_mid.Y       , pt_mid.Z)

            # Move on X Axis
            if not (room.IsPointInRoom(pt_up) and room.IsPointInRoom(pt_down)):
                if room.IsPointInRoom(pt_up):
                    move_room_and_tag(tag, room, pt_up)

                elif room.IsPointInRoom(pt_down):
                    move_room_and_tag(tag, room, pt_down)


            # Move on Y Axis
            elif not(room.IsPointInRoom(pt_right) and room.IsPointInRoom(pt_left)):
                if room.IsPointInRoom(pt_right):
                    move_room_and_tag(tag, room, pt_right)

                elif room.IsPointInRoom(pt_left):
                    move_room_and_tag(tag, room, pt_left)
    t.Commit()