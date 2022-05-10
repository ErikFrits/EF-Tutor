# -*- coding: utf-8 -*-

# IMPORTS
from Autodesk.Revit.DB import * # Import everything from DB (Very good for beginners and development)

# VARIABLES
app     = __revit__.Application

# FUNCTIONS
def convert_internal_to_m(length):
    """Function to convert internal units to meters.
    :param length: Length in internal Revit Units
    :return: Length in Meters, rounded to 2nd digit"""
    rvt_year = int(app.VersionNumber)

    # RVT < 2022
    if rvt_year < 2022:
        return UnitUtils.Convert(length,
                                 DisplayUnitType.DUT_DECIMAL_FEET,
                                 DisplayUnitType.DUT_METERS) # Change to any other unit here...
    # RVT >= 2022
    else:
        return UnitUtils.ConvertFromInternalUnits(length,
                                                  UnitTypeId.Meters)