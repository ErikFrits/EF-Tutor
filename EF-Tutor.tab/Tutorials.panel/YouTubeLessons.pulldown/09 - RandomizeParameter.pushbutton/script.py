# -*- coding: utf-8 -*-
__title__ = "09 - Randomize Parameter (+ Custom UI)"
__doc__ = """Date    = 22.04.2023
Randomize Parameter Values for specific Families
_____________________________________________________________________
Author: Erik Frits"""
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
import random
from Autodesk.Revit.DB           import *
from Autodesk.Revit.UI           import UIDocument, UIApplication

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
uidoc        = __revit__.ActiveUIDocument           #type: UIDocument
doc          = __revit__.ActiveUIDocument.Document  #type: Document
app          = __revit__.Application                #type: UIApplication
rvt_year     = int(app.VersionNumber)

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
#==================================================
def get_elements_by_type_name(type_name):
    """Function to get Elements by Type Name."""

    # CREATE RULE
    param_id    = ElementId(BuiltInParameter.ALL_MODEL_TYPE_NAME)
    f_param     = ParameterValueProvider(param_id)
    f_evaluator = FilterStringEquals()
    f_rule      = FilterStringRule(f_param, f_evaluator  , type_name, True)
    # Revit 2023 does not need last argument in f_rule!

    # CREATE FILTER
    filter_type_name = ElementParameterFilter(f_rule)

    # GET ELEMENTS
    return FilteredElementCollector(doc).WherePasses(filter_type_name)\
                          .WhereElementIsNotElementType().ToElements()



def get_elements_by_family_name(family_name):
    """Function to get Elements by Family Name."""

    # CREATE RULE
    param_id    = ElementId(BuiltInParameter.ALL_MODEL_TYPE_NAME)
    f_param     = ParameterValueProvider(param_id)
    f_evaluator = FilterStringEquals()
    f_rule      = FilterStringRule(f_param, f_evaluator  , family_name, True)
    # Revit 2023 does not need last argument in f_rule!

    # CREATE FILTER
    filter_family_name = ElementParameterFilter(f_rule)

    # GET ELEMENTS
    return FilteredElementCollector(doc).WherePasses(filter_family_name)\
                               .WhereElementIsNotElementType().ToElements()


def convert_internal_units(value, get_internal = True, units='m'):
    #type: (float, bool, str) -> float
    """Function to convert Internal units to meters or vice versa.
    :param value:        Value to convert
    :param get_internal: True to get internal units, False to get Meters
    :param units:        Select desired Units: ['m', 'm2']
    :return:             Length in Internal units or Meters."""

    if rvt_year >= 2021:
        from Autodesk.Revit.DB import UnitTypeId
        if   units == 'm' : units = UnitTypeId.Meters
        elif units == "m2": units = UnitTypeId.SquareMeters
        elif units == 'cm': units = UnitTypeId.Centimeters
    else:
        from Autodesk.Revit.DB import DisplayUnitType
        if   units == 'm' : units = DisplayUnitType.DUT_METERS
        elif units == "m2": units = DisplayUnitType.DUT_SQUARE_METERS
        elif units == "cm": units = DisplayUnitType.DUT_CENTIMETERS

    if get_internal:
        return UnitUtils.ConvertToInternalUnits(value, units)
    return UnitUtils.ConvertFromInternalUnits(value, units)

def random_step(_min, _max, _step):
    return random.randrange(_min, _max+1, _step)


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================

# 1️⃣ Variables
# family_name = 'Vertical Blade'
# type_name   = 'Vertical Blade'
# param_name  = 'Tiefe'
# _min        = 40
# _max        = 250
# _step       = 10

# 🔷 Bonus: Custom UI
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button, CheckBox)

# Define UI Components
components = [Label("Element's Type Name:"), TextBox('type_name', Text="Vertical Blade"),
              Label('Parameter Name:'), TextBox('param_name', Text="Tiefe"),
              Separator(),
              Label('Min Value(in cm):'), TextBox('_min', Text="40"),
              Label('Max Value(in cm):'), TextBox('_max', Text="250"),
              Label('Step Value(in cm):'), TextBox('_step', Text="10"),
              Separator(),
              Button('Select')]

# Create UI Form + Show it
form = FlexForm(__title__, components)
form.show()

# Get All Values (as dict)
values = form.values

# Read Values
type_name   = values['type_name']
param_name  = values['param_name']
_min        = float(values['_min'])
_max        = float(values['_max'])
_step       = float(values['_step'])



# 2️⃣ Get Elements
elements = get_elements_by_type_name(type_name)
# elements = get_elements_by_family_name(family_name)


# 3️⃣ Write Random Parmaeter Values

t = Transaction(doc, __title__)
t.Start() #🔓

for el in elements:
    p = el.LookupParameter(param_name)
    if p:
        value_cm = random_step(_min, _max, _step)
        value_ft = convert_internal_units(value_cm, get_internal=True, units='cm')
        p.Set(value_ft)

t.Commit() #🔒
