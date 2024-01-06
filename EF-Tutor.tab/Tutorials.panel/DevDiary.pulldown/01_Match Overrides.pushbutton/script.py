# -*- coding: utf-8 -*-
__title__ = "01 - Match Override Graphics"                                # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 22.05.2022
_____________________________________________________________________
Description:
Match Graphic Overviews
_____________________________________________________________________
How-to:
-> Run the tool
-> Select main element
-> Match other elements 

_____________________________________________________________________
Video Tutorial is available on my Patreon: www.patreon.com/ErikFrits
Click F1 while hovering this button to open the link."""                # Button Description shown in Revit UI
__helpurl__ = 'https://www.patreon.com/posts/01-dev-diary-66841678'

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc     = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc   = __revit__.ActiveUIDocument            # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app     = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

# Pick Main Element
with forms.WarningBar(title='Pick Main Element:'):
    main_elem = revit.pick_element()
if not main_elem:
    forms.alert("No element was selected. Please Try Again.", title=__title__, exitscript=True)

# Get Main GraphicsOverrides
graphics = doc.ActiveView.GetElementOverrides(main_elem.Id)

# Loop keep selecting elements to match
with forms.WarningBar(title='Pick Elements to match Graphics:', handle_esc=True):
    while True:
        elem = None
        try:
            elem = revit.pick_element()
        except:
            break
        if not elem: break

        # Set GraphicsOverrides
        t = Transaction(doc, __title__)
        t.Start()
        doc.ActiveView.SetElementOverrides(elem.Id, graphics)
        t.Commit()
