# -*- coding: utf-8 -*-
__title__ = "02 - Element Information"
__doc__ = """This is a simple tool to pick an element and 
print out some simple information about it. 
It's part of my YouTube RevitAPI Tutorial.
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
import sys
from Autodesk.Revit.DB import *

#pyRevit
from pyrevit import forms, revit

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================
# print('Hello World!')

# BONUS: pyRevit Input
# selected_views = forms.select_views()
# if selected_views:
#     print(selected_views)

# PICK ELEMENT

with forms.WarningBar(title='Pick an Element:'):
    element      = revit.pick_element()

element_type = type(element)

if element_type != Wall:
    forms.alert('You were supposed to pick a Wall.', exitscript=True)

# print(element)
# print(element_type)

# GET INFORMATION
e_cat       = element.Category.Name
e_id        = element.Id
e_level     = doc.GetElement(element.LevelId)
e_wall_type = element.WallType
e_width     = element.Width

# PRINT CONSOLE
print('Element Category: {}'.format(e_cat))
print('ElementId: {}'.format(e_id))
print('ElementLevelId: {}'.format(e_level.Name))
print('Wall WallType: {}'.format(e_wall_type))
print('Wall Width: {}'.format(e_width))




# pyCharm Shortcut: CTRL + B <- Show where object is declared
# pyCharm Shortcut: CTRL + Q <- Read doc string of objects
