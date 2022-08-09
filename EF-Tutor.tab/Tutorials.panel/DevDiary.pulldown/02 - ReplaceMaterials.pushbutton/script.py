# -*- coding: utf-8 -*-
__title__ = "02 - Replace Materials"
__doc__ = """This tool will replace Material A with Material B.
It is part of the Dev Diary video availabel on my Patreon, 
where I document how i write my tools.
You can access it by signing up on:
www.patreon.com/ErikFrits"""
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

import clr
clr.AddReference('System')
from System.Collections.Generic import List

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

# GET ALL MATERIALS
all_materials = FilteredElementCollector(doc).OfClass(Material).ToElements()

# GET MATERIAL A/B
mat_A = all_materials[0]
mat_B = all_materials[1]


# GET WALLS/FLOORS/ ROOFS
excl_families = ['Curtain Wall', 'Stacked Wall', 'Sloped Glazing']

all_walls  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsElementType().ToElements()
all_floors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsElementType().ToElements()
all_roofs  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Roofs).WhereElementIsElementType().ToElements()
all_types  = list(all_walls) + list(all_floors) + list(all_roofs)
all_types  = [t for t in all_types if t.FamilyName not in excl_families] # EXCLUDE TYPES WITHOUT STRUCTURE LAYERS
all_types  = [t for t in all_types if type(t) != FamilySymbol]           # REMOVE MODEL IN-PLACE ELEMENTS

# GET USED MATERIALS
t = Transaction(doc, __title__)
t.Start()

count = 0
for typ in all_types:
    structure = typ.GetCompoundStructure() # This is just a copy. It's not related to any Types
    layers    = structure.GetLayers()

    for layer in layers:
        mat_id = layer.MaterialId
        if mat_id == ElementId(-1):
            continue

        mat      = doc.GetElement(mat_id)
        mat_name = mat.Name


        # REPLACE MATERIALS
        inx        = layer.LayerId
        structure.SetMaterialId(inx, mat_B.Id)  # We are modifying our structure copy
        typ.SetCompoundStructure(structure)     # Finally we need to assign our new structure to the type.
        count += 1

        # REPORT CHANGES
        print('Changed: {} -> {}'.format(mat_name, mat_B.Name))
        print('In total {} materials have been renamed.'.format(count))

t.Commit()
