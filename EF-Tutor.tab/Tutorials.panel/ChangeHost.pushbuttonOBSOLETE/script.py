# -*- coding: utf-8 -*-
__title__ = "Change Host"
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
from pyrevit import forms
from Autodesk.Revit.DB.Architecture import TopographySurface
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
# def get_elements_by_type_name(type_name):
#     """Function to get Elements by Type Name."""
#
#     # CREATE RULE
#     param_id    = ElementId(BuiltInParameter.ALL_MODEL_TYPE_NAME)
#     f_param     = ParameterValueProvider(param_id)
#     f_evaluator = FilterStringEquals()
#     f_rule      = FilterStringRule(f_param, f_evaluator  , type_name, True)
#     # Revit 2023 does not need last argument in f_rule!
#
#     # CREATE FILTER
#     filter_type_name = ElementParameterFilter(f_rule)
#
#     # GET ELEMENTS
#     return FilteredElementCollector(doc).WherePasses(filter_type_name)\
#                           .WhereElementIsNotElementType().ToElements()
#
#
#
# def get_elements_by_family_name(family_name):
#     """Function to get Elements by Family Name."""
#
#     # CREATE RULE
#     param_id    = ElementId(BuiltInParameter.ALL_MODEL_TYPE_NAME)
#     f_param     = ParameterValueProvider(param_id)
#     f_evaluator = FilterStringEquals()
#     f_rule      = FilterStringRule(f_param, f_evaluator  , family_name, True)
#     # Revit 2023 does not need last argument in f_rule!
#
#     # CREATE FILTER
#     filter_family_name = ElementParameterFilter(f_rule)
#
#     # GET ELEMENTS
#     return FilteredElementCollector(doc).WherePasses(filter_family_name)\
#                                .WhereElementIsNotElementType().ToElements()
#
#
# def convert_internal_units(value, get_internal = True, units='m'):
#     #type: (float, bool, str) -> float
#     """Function to convert Internal units to meters or vice versa.
#     :param value:        Value to convert
#     :param get_internal: True to get internal units, False to get Meters
#     :param units:        Select desired Units: ['m', 'm2']
#     :return:             Length in Internal units or Meters."""
#
#     if rvt_year >= 2021:
#         from Autodesk.Revit.DB import UnitTypeId
#         if   units == 'm' : units = UnitTypeId.Meters
#         elif units == "m2": units = UnitTypeId.SquareMeters
#         elif units == 'cm': units = UnitTypeId.Centimeters
#     else:
#         from Autodesk.Revit.DB import DisplayUnitType
#         if   units == 'm' : units = DisplayUnitType.DUT_METERS
#         elif units == "m2": units = DisplayUnitType.DUT_SQUARE_METERS
#         elif units == "cm": units = DisplayUnitType.DUT_CENTIMETERS
#
#     if get_internal:
#         return UnitUtils.ConvertToInternalUnits(value, units)
#     return UnitUtils.ConvertFromInternalUnits(value, units)
#
# def random_step(_min, _max, _step):
#     return random.randrange(_min, _max+1, _step)


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


# GET ELEMENTS
selection = uidoc.Selection.GetElementIds()
elements = [doc.GetElement(e_id) for e_id in selection]

trees = []
topo = None

for i in elements:
    if type(i) == FamilyInstance:       trees.append(i)
    elif type(i) == TopographySurface:  topo = i

if not topo or not trees:
    forms.alert('No Topo or Trees selected',__title__, exitscript=True)




for tree in trees:
    # Tree Line
    pt = tree.Location.Point

    print(topo.ContainsPoint(pt))
