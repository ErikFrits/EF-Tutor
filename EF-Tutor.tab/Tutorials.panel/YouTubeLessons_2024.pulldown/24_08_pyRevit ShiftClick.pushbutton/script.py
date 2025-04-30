# -*- coding: utf-8 -*-
__title__   = "8 - pyRevit Button Modes"
__doc__     = """Version = 1.0
Date    = 15.06.2024
________________________________________________________________
Description:

Learn about pyRevit buttons modes that allow you to execute 
different code depending on the click mode:
- Regular Click
- Shift Click
- CTRL Click

________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

from pyrevit import EXEC_PARAMS


if EXEC_PARAMS.config_mode:
    print('Shift Click Activated')
    print('Executing Code...')

elif EXEC_PARAMS.debug_mode:
    print('CTRL Click Activated')
    print('Executing Code...')
else:
    print('Regular Click Activated')
    print('Executing Code...')



