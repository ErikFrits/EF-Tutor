# -*- coding: utf-8 -*-
__title__ = "10 - ElementParameterFilter"
__doc__ = """Version = 1.0
Date    = 11.11.2023
_____________________________________________________________________
Description:
Example of using ElementParameterFilter.
- Get Element by Type Name
- Get Element by Family Name
- Get Walls higher than x Meters
_____________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
#
# #1️⃣ Parameter
# p_fam_id = ElementId(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM)
# f_param  = ParameterValueProvider(p_fam_id)
#
# #2️⃣ Evaluator
# evaluator = FilterStringContains()
#
# #3️⃣ Value
# value = 'FE TÜR'
#
# #4️⃣ Rule
# rvt_year = int(app.VersionNumber)
# if rvt_year >= 2023:
#     f_rule = FilterStringRule(f_param, evaluator, value)
# else:
#     f_rule = FilterStringRule(f_param, evaluator, value, False)
#
#
# #5️⃣ Filter
# filter_fam_name = ElementParameterFilter(f_rule)
#
# #6️⃣ Apply Filter to FEC
# element_ids = FilteredElementCollector(doc)\
#                 .OfCategory(BuiltInCategory.OST_Windows)\
#                 .WherePasses(filter_fam_name)\
#                 .WhereElementIsNotElementType()\
#                 .ToElementIds()
#
# #👉 Select Elements
# uidoc.Selection.SetElementIds(element_ids)











def get_elements_by_family_name(family_name):
    """Function to get Elements by Family Name"""
    #1️⃣ Parameter
    p_fam_id = ElementId(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM)
    f_param  = ParameterValueProvider(p_fam_id)

    #2️⃣ Evaluator
    evaluator = FilterStringEquals()

    #3️⃣ Value
    value = family_name

    #4️⃣ Rule
    rvt_year = int(app.VersionNumber)
    if rvt_year >= 2023:
        f_rule = FilterStringRule(f_param, evaluator, value)
    else:
        f_rule = FilterStringRule(f_param, evaluator, value, False)


    #5️⃣ Filter
    filter_fam_name = ElementParameterFilter(f_rule)

    #6️⃣ Apply Filter to FEC
    return FilteredElementCollector(doc)\
                    .WherePasses(filter_fam_name)\
                    .WhereElementIsNotElementType()\
                    .ToElements()


def get_elements_by_type_name(type_name):
    """Function to get Elements by Family Name"""
    #1️⃣ Parameter
    p_type_id = ElementId(BuiltInParameter.SYMBOL_NAME_PARAM)
    f_param  = ParameterValueProvider(p_type_id)

    #2️⃣ Evaluator
    evaluator = FilterStringEquals()

    #3️⃣ Value
    value = type_name

    #4️⃣ Rule
    rvt_year = int(app.VersionNumber)
    if rvt_year >= 2023:
        f_rule = FilterStringRule(f_param, evaluator, value)
    else:
        f_rule = FilterStringRule(f_param, evaluator, value, False)


    #5️⃣ Filter
    filter_fam_name = ElementParameterFilter(f_rule)

    #6️⃣ Apply Filter to FEC
    return FilteredElementCollector(doc)\
                    .WherePasses(filter_fam_name)\
                    .WhereElementIsNotElementType()\
                    .ToElements()

# MAIN
elements    = get_elements_by_type_name('2000 x 2250')
el_ids      = [el.Id for el in elements]
List_el_ids = List[ElementId](el_ids)

uidoc.Selection.SetElementIds(List_el_ids)


# ╔═╗╦ ╦╔═╗╦═╗╔═╗╔╦╗  ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗╔═╗
# ╚═╗╠═╣╠═╣╠╦╝║╣  ║║  ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝╚═╗
# ╚═╝╩ ╩╩ ╩╩╚═╚═╝═╩╝  ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═╚═╝

def get_elements_by_shared_p_value(s_param_name, value):
    """Function to get Elements by Family Name"""
    #1️⃣Shared Parameter
    rule   = ParameterFilterRuleFactory.CreateSharedParameterApplicableRule(s_param_name)
    filter = ElementParameterFilter(rule)

    p_type_id = ElementId(BuiltInParameter.SYMBOL_NAME_PARAM)
    f_param  = ParameterValueProvider(p_type_id)

    #2️⃣ Evaluator
    evaluator = FilterStringEquals()

    #3️⃣ Value
    value = value

    #4️⃣ Rule
    rvt_year = int(app.VersionNumber)
    if rvt_year >= 2023:
        f_rule = FilterStringRule(f_param, evaluator, value)
    else:
        f_rule = FilterStringRule(f_param, evaluator, value, False)


    #5️⃣ Filter
    filter_fam_name = ElementParameterFilter(f_rule)

    #6️⃣ Apply Filter to FEC
    return FilteredElementCollector(doc)\
                    .WherePasses(filter_fam_name)\
                    .WhereElementIsNotElementType()\
                    .ToElements()
