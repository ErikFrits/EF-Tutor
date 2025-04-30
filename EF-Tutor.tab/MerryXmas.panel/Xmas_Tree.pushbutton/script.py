# -*- coding: utf-8 -*-
__title__ = "🌲X-Mas Tree"
__doc__ = """Version = 1.0
Date    = 15.06.2024
________________________________________________________________
Description:
Creates a multi-tier, overlapping Christmas Tree with a trunk and 
several conical segments. A sphere is placed on top as a 'star'.
________________________________________________________________
Author: Erik Frits
"""

from Autodesk.Revit.DB import *

import clr
clr.AddReference('System')
from System.Collections.Generic import List
import math

app   = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc   = uidoc.Document  # type: Document


# --------------------------------------------------------------------------
# HELPER: Create revolve-based conical geometry
# --------------------------------------------------------------------------
def CreateRevolvedSolid_Conical(origin, baseZ, topZ, baseRadius):
    """
    Creates a conical revolve from baseZ to topZ, tapering from baseRadius
    down to zero at the top. Revolve around the global Z-axis for 360 degrees.
    """
    frame  = Frame(origin, XYZ.BasisX, XYZ.BasisY, XYZ.BasisZ)

    profileloops = List[CurveLoop]()
    profileloop  = CurveLoop()

    # Triangle cross-section:
    # (0,0,baseZ) -> (0,0,topZ) -> (baseRadius,0,baseZ) -> back to start
    p1 = XYZ(origin.X, origin.Y, baseZ)
    p2 = XYZ(origin.X, origin.Y, topZ)
    p3 = XYZ(origin.X + baseRadius, origin.Y, baseZ)

    profileloop.Append(Line.CreateBound(p1, p2))
    profileloop.Append(Line.CreateBound(p2, p3))
    profileloop.Append(Line.CreateBound(p3, p1))

    profileloops.Add(profileloop)

    return GeometryCreationUtilities.CreateRevolvedGeometry(frame, profileloops, 0, 2 * math.pi)


# --------------------------------------------------------------------------
# HELPER: Create revolve-based cylindrical geometry
# --------------------------------------------------------------------------
def CreateRevolvedSolid_Cylindrical(origin, baseZ, topZ, radius):
    """
    Creates a cylindrical revolve from baseZ to topZ with a given radius,
    revolving around the global Z-axis for 360 degrees.
    """
    frame  = Frame(origin, XYZ.BasisX, XYZ.BasisY, XYZ.BasisZ)

    profileloops = List[CurveLoop]()
    profileloop  = CurveLoop()

    # Rectangle cross-section in the Z-direction:
    # (0,0,baseZ) -> (0,0,topZ) -> (radius,0,topZ) -> (radius,0,baseZ)
    p1 = XYZ(origin.X, origin.Y, baseZ)
    p2 = XYZ(origin.X, origin.Y, topZ)
    p3 = XYZ(origin.X+radius,   origin.Y, topZ)
    p4 = XYZ(origin.X+radius,   origin.Y, baseZ)

    profileloop.Append(Line.CreateBound(p1, p2))
    profileloop.Append(Line.CreateBound(p2, p3))
    profileloop.Append(Line.CreateBound(p3, p4))
    profileloop.Append(Line.CreateBound(p4, p1))

    profileloops.Add(profileloop)

    return GeometryCreationUtilities.CreateRevolvedGeometry(
        frame,
        profileloops,
        0,
        2 * math.pi
    )


# --------------------------------------------------------------------------
# HELPER: Create a revolve-based sphere (by revolving a semicircle)
# --------------------------------------------------------------------------
def CreateCenterBasedSphere(center, radius):
    """
    Creates a sphere by revolving a semicircle around the global Z axis.
    """
    frame = Frame(center, XYZ.BasisX, XYZ.BasisY, XYZ.BasisZ)

    profileloops = List[CurveLoop]()
    profileloop  = CurveLoop()

    # Semicircle in the XZ plane
    semiEllipse = Ellipse.CreateCurve(
        center,
        radius,
        radius,
        XYZ.BasisX,
        XYZ.BasisZ,
        -math.pi / 2.0,
         math.pi / 2.0
    )
    profileloop.Append(semiEllipse)

    # Straight line closing the semicircle profile
    topPt    = XYZ(center.X, center.Y, center.Z + radius)
    bottomPt = XYZ(center.X, center.Y, center.Z - radius)
    profileloop.Append(Line.CreateBound(topPt, bottomPt))

    profileloops.Add(profileloop)

    return GeometryCreationUtilities.CreateRevolvedGeometry(
        frame,
        profileloops,
        -math.pi,
        math.pi
    )


# --------------------------------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------------------------------
origin = uidoc.Selection.PickPoint("Pick a base point for the Christmas Tree")

# --------------------------------------------------------------------------
# SCALING FACTOR
# --------------------------------------------------------------------------
scaleFactor = 5.0  # <--- Multiply all dimensions below by this factor

# Basic parameters
trunkHeight    = 0.5  * scaleFactor
trunkRadius    = 0.08 * scaleFactor
treeHeight     = 2.0  * scaleFactor   # total height for the conical portion
treeBaseRadius = 0.5  * scaleFactor   # radius for the bottom cone
sphereRadius   = 0.15 * scaleFactor   # decorative sphere on top

# Multi-cone parameters
numCones       = 8
overlap        = 0.1  * scaleFactor   # how much each cone overlaps the one below (in Z)

# --------------------------------------------------------------------------
# 1) Create a trunk (small cylinder)
# --------------------------------------------------------------------------
trunkBaseZ = origin.Z
trunkTopZ  = trunkBaseZ + trunkHeight
trunkGeom  = CreateRevolvedSolid_Cylindrical(origin=origin,baseZ = trunkBaseZ,topZ  = trunkTopZ,radius= trunkRadius)

# --------------------------------------------------------------------------
# 2) Create multiple overlapping conical tiers
# --------------------------------------------------------------------------
# finalTop = trunkTopZ + numCones*coneHeight - (numCones - 1)*overlap
# we want finalTop = trunkTopZ + treeHeight
#
# => numCones*coneHeight - (numCones - 1)*overlap = treeHeight
# => coneHeight = (treeHeight + (numCones - 1)*overlap) / numCones

coneHeight = (treeHeight + (numCones - 1)*overlap) / float(numCones)

allCones = []
for i in range(numCones):
    coneBaseZ = trunkTopZ + i*(coneHeight - overlap)
    coneTopZ  = coneBaseZ + coneHeight

    # Decreasing radius from treeBaseRadius at bottom cone to ~20% at top
    fractionUp   = float(i) / (numCones - 1) if numCones > 1 else 0
    # We'll reduce to 20% at the final (top) cone:
    radiusFactor = 1.0 - 0.8 * fractionUp
    thisRadius   = treeBaseRadius * radiusFactor

    coneGeom = CreateRevolvedSolid_Conical(origin=origin, baseZ = coneBaseZ, topZ = coneTopZ, baseRadius = thisRadius)
    allCones.append(coneGeom)



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
# --------------------------------------------------------------------------
# Combine all geometry
# --------------------------------------------------------------------------
finalGeometry = [trunkGeom] + allCones

# Transaction
t = Transaction(doc, 'Create Overlapping Xmas Tree')
t.Start()

ds_trunk = DirectShape.CreateElement(doc, ElementId(BuiltInCategory.OST_GenericModel))
ds_trunk.SetShape([trunkGeom])

ds_tree = DirectShape.CreateElement(doc, ElementId(BuiltInCategory.OST_GenericModel))
ds_tree.SetShape(allCones)


paint_ds(ds_trunk, Color(150,150,100))
paint_ds(ds_tree, Color(140,190,130))


t.Commit()
