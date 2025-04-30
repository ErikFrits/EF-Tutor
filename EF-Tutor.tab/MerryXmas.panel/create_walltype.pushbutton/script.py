# -*- coding: utf-8 -*-
__title__   = "New WallType"
__doc__     = """Version = 1.0
Date    = 17.01.2025
________________________________________________________________
Description:
- Select Wall
- Split Into Individual Layers
________________________________________________________________

To-Do:
- Supress Join walls Warning
- Keep same Mark Parameter (+Supress Mark Parameter Warning)
________________________________________________________________
Authors: Erik Frits / Mohamed Bedair"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#====================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from pyrevit import forms

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#====================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
#====================================================================================================

t = Transaction(doc, 'NewType')
t.Start()


# Duplicate Existing WallType
random_wall_type = FilteredElementCollector(doc).OfClass(WallType).FirstElement()
new_name         = "EF Super-Duper Concrete Wall 3000"
new_wall_type    = random_wall_type.Duplicate(new_name)

# Specify Layer Properties
layer_func  = MaterialFunctionAssignment.Structure
layer_width_ft = UnitUtils.ConvertToInternalUnits(10, UnitTypeId.Centimeters) # 10cm-> feet
random_mat  = FilteredElementCollector(doc).OfClass(Material).FirstElement() # Select Specific Material

# Create layers (I make same one as example)
layer_a = CompoundStructureLayer(layer_width_ft, layer_func, random_mat.Id)
layer_b = CompoundStructureLayer(layer_width_ft, layer_func, random_mat.Id)
layers  = [layer_a, layer_b]

# Create+Set Material Compound Structure for Wall Type
structure = CompoundStructure.CreateSimpleCompoundStructure(layers)
new_wall_type.SetCompoundStructure(structure)

print(new_wall_type)
t.Commit()




all_walls_types = FilteredElementCollector(doc).OfClass(WallType).ToElements()
dict_wall_types = {Element.Name.GetValue(typ):typ for typ in all_walls_types}

type_name       = 'EF Super-Duper Concrete Wall 3000'

if type_name in dict_wall_types:
    wall_type = dict_wall_types[type_name]








