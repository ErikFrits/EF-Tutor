# -*- coding: utf-8 -*-

# IMPORTS
from Autodesk.Revit.DB import *

# VARIABLES
uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document

# FUNCTIONS

def get_selected_elements(uidoc):
    """This function will return elements that are currently selected in Revit UI
    :param uidoc:   uidoc where elements are selected.
    :return:        List of selected elements"""
    return [uidoc.Document.GetElement(elem_id) for elem_id in uidoc.Selection.GetElementIds()]
