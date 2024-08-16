# -*- coding: utf-8 -*-
__title__ = '3 - CoordSystems'

# Imports
from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#--------------------------------------------------
uidoc     = __revit__.ActiveUIDocument
doc       = __revit__.ActiveUIDocument.Document  #type: Document

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ Functions
#--------------------------------------------------
def convert_internal_units(value, get_internal=True):
    # type: (float, bool) -> float
    """Function to convert Internal units to meters or vice versa.
    :param value:        Value to convert
    :param get_internal: True - Convert TO Internal / Flase - Convert FROM Internal
    :return:             Length in Internal units or Meters."""
    if get_internal:
        return UnitUtils.ConvertToInternalUnits(value, UnitTypeId.Meters)
    return UnitUtils.ConvertFromInternalUnits(value, UnitTypeId.Meters)


# ╔═╗╦  ╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝ CLASS
#--------------------------------------------------
class PointConverter:
    pt_internal = None
    pt_survey   = None
    pt_project  = None

    def __init__(self, x, y, z, coord_sys='internal', input_units = 'm'):
        # type:( float, float, float, str, str)
        """ PointConverter - Convert coordinate into desired coordinate system.
        Args:
            x : Float in meters representing the x-coordinate.
            y : Float in meters representing the y-coordinate.
            z : Float in meters representing the z-coordinate.
            coord_sys : Coordinate System of provided coordinates.
                        Possible values: 'internal'/'project'/'survey'
            input_units : Float in meters representing the z-coordinate.
                          Possible Values: 'm' / 'ft' """

        # Get Systems Transform
        srvTrans  = self.GetSurveyTransform()
        projTrans = self.GetProjectTransform()


        # Convert to Internal Units
        if input_units == 'm':
            x = convert_internal_units(x, get_internal=True) # Convert Units to Internal
            y = convert_internal_units(y, get_internal=True) # Convert Units to Internal
            z = convert_internal_units(z, get_internal=True) # Convert Units to Internal

        # 1️⃣INTERNAL COORDINATE SYSTEM
        if coord_sys.lower() == 'internal':
            self.pt_internal = XYZ(x, y, z)
            self.pt_survey   = self.ApplyInverseTransformation(srvTrans , self.pt_internal)
            self.pt_project  = self.ApplyInverseTransformation(projTrans, self.pt_internal)

        # 2️⃣PROJECT COORDINATE SYSTEM
        elif coord_sys.lower() == 'project':
            self.pt_project    = XYZ(x, y, z)
            self.pt_internal   = self.ApplyTransformation(projTrans, self.pt_project)
            self.pt_survey     = self.ApplyInverseTransformation(srvTrans, self.pt_internal)

        # 3️⃣SURVEY COORDINATE SYSTEM
        elif coord_sys.lower() == 'survey':
            self.pt_survey     = XYZ(x, y, z)
            self.pt_internal   = self.ApplyTransformation(srvTrans, self.pt_survey)
            self.pt_project     = self.ApplyInverseTransformation(projTrans, self.pt_internal)

        else: raise Exception("Wrong argument value for 'coord_sys' in PointConverter class.")

    #⛑ HELPING METHODS
    def GetSurveyTransform(self):
        """Gets the Active Project Locations Transform (Survey)."""
        return doc.ActiveProjectLocation.GetTotalTransform()

    def GetProjectTransform(self):
        """Get the Project Base Points Transform."""
        basePtLoc = next((l for l in FilteredElementCollector(doc) \
                         .OfClass(ProjectLocation) \
                         .WhereElementIsNotElementType() \
                         .ToElements() if l.Name in ['Project', 'Projekt']), None)
        return basePtLoc.GetTotalTransform()

    def ApplyInverseTransformation(self, t, pt):
        """Applies the inverse transformation of
        the given Transform to the given point."""
        return t.Inverse.OfPoint(pt)

    def ApplyTransformation(self, t, pt):
        """Applies the transformation of
        the given Transform to the given point."""
        return t.OfPoint(pt)

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
# EXAMPLE ON HOW TO USE:

# 😉 Helper Function
def print_coord_in_m(pt, prefix=""):
    #type: (XYZ, str)
    """Helper Function to display Point Coordinates
    in Meters to compare to Coordinates displayed in Revit."""
    x = round(convert_internal_units(pt.X, get_internal=False), 4)
    y = round(convert_internal_units(pt.Y, get_internal=False), 4)
    z = round(convert_internal_units(pt.Z, get_internal=False), 4)
    # print(prefix, 'N/S:{}'.format(y), 'E/W:{}'.format(x), 'Elev:{}'.format(z))
    print(prefix, 'X:{}'.format(x), 'Y:{}'.format(y), 'Z:{}'.format(z))
# --------------------------------------------------------------

# 1️⃣ Define Coordinates Manually
# X = 0    # EW Coordinate
# Y = 0    # NS Coordinate
# Z = 0    # Elevation

# 1️⃣ Pick Point
picked_point = uidoc.Selection.PickPoint()
X = picked_point.X
Y = picked_point.Y
Z = picked_point.Z

# 2️⃣ Create PointConverter instance
converter = PointConverter(X, Y, Z, coord_sys='internal', input_units='ft')

# 3️⃣ Converted Points
pt_internal = converter.pt_internal
pt_project  = converter.pt_project
pt_survey   = converter.pt_survey

# 👀 Display Results
print_coord_in_m(pt_internal, prefix='Internal: ')
print_coord_in_m(pt_project,  prefix='Project: ')
print_coord_in_m(pt_survey,   prefix='Survey: ')

Author = 'Erik Frits'