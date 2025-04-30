# -*- coding: utf-8 -*-
__title__   = "❄️X-Mas Ornament"
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
from Autodesk.Revit.UI.Selection import ObjectSnapTypes, ObjectType
import clr, math

clr.AddReference('System')
from System.Collections.Generic import List


def CreateCenterbasedSphere(center, radius):
    frame = Frame(center,
                  XYZ.BasisX,
                  XYZ.BasisY,
                  XYZ.BasisZ)

    profileloops = List[CurveLoop]()
    profileloop = CurveLoop()

    cemiEllipse = Ellipse.CreateCurve(center, radius, radius,
                                      XYZ.BasisX,
                                      XYZ.BasisZ,
                                      -math.pi / 2.0, math.pi / 2.0)

    profileloop.Append(cemiEllipse);
    profileloop.Append(Line.CreateBound(
        XYZ(center.X, center.Y, center.Z + radius),
        XYZ(center.X, center.Y, center.Z - radius)))
    profileloops.Add(profileloop);

    return GeometryCreationUtilities.CreateRevolvedGeometry(frame, profileloops, -math.pi, math.pi)




def pick_point_on_geo():
    """Prompt user to select point on Element's Geometry."""
    # 1. Prompt PickObject with PointOnElement option
    from Autodesk.Revit.UI.Selection import ObjectType
    pt_ref = uidoc.Selection.PickObject(ObjectType.PointOnElement)

    # 2. Get element's Geometry from Picked Point
    element = doc.GetElement(pt_ref)
    geo     = element.GetGeometryObjectFromReference(pt_ref)

    if geo:
        uv = pt_ref.UVPoint
        pt = geo.Evaluate(uv)
        return pt



# print(sphere)

import random

def random_color():
    # Define a list of RGB color tuples
    colors = [
        (255, 100, 100), # Red
        (100, 255, 100), # Green
        (100, 100, 255), # Blue
        (255, 255, 100), # Yellow
        (255, 100, 255), # Magenta
        (255, 150, 50),  # Orange
    ]

    # Select a random color from the list
    selected_color = random.choice(colors)

    color = Color(selected_color[0], selected_color[1], selected_color[2])

    return color




def paint_ds(ds, color):
    # Get Solid Pattern
    all_pats = FilteredElementCollector(doc).OfClass(FillPatternElement).ToElements()
    all_solid = [pat for pat in all_pats if pat.GetFillPattern().IsSolidFill]
    solid_pattern = all_solid[0]

    # Create GraphicSettings with Color
    ogs = OverrideGraphicSettings()
    ogs.SetSurfaceBackgroundPatternColor(color)
    ogs.SetSurfaceBackgroundPatternId(solid_pattern.Id)

    # Set Color
    doc.ActiveView.SetElementOverrides(ds.Id, ogs)


list_balls = []

for i in range(155):
    try:

        # Get Point
        pt = pick_point_on_geo()

        # Create Sphere Geo
        r = 0.2
        sphere = CreateCenterbasedSphere(pt, r)

        # Transaction
        t = Transaction(doc, 'test')
        t.Start()

        # Create DS Shape
        ds_ball = DirectShape.CreateElement(doc, ElementId(BuiltInCategory.OST_GenericModel))
        ds_ball.SetShape([sphere])

        list_balls.append(ds_ball)

        for ds in list_balls:
            color = random_color()
            paint_ds(ds, color)

        t.Commit()
    except:
        break















print('Test')








all_walls       = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
all_floors      = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
all_floor_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsElementType().ToElements()
























