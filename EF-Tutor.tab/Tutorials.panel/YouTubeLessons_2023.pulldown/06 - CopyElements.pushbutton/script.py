# -*- coding: utf-8 -*-
__title__   = "06 - Copy Elements"
__doc__ = """Date    = 22.10.2022
_____________________________________________________________________
Description:
Script from a YouTube Tutorial about copying Elements.
_____________________________________________________________________
Author:  Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#=======================================================================================
from Autodesk.Revit.DB import *

#pyRevit
from pyrevit.forms import select_views

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#=======================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

#🟢 ╔═╗╔═╗╔═╗╦ ╦  ╦ ╦╦╔╦╗╦ ╦  ╦  ╦╔═╗╔═╗╔╦╗╔═╗╦═╗
#🟢 ║  ║ ║╠═╝╚╦╝  ║║║║ ║ ╠═╣  ╚╗╔╝║╣ ║   ║ ║ ║╠╦╝
#🟢 ╚═╝╚═╝╩   ╩   ╚╩╝╩ ╩ ╩ ╩   ╚╝ ╚═╝╚═╝ ╩ ╚═╝╩╚═ COPY WITH VECTOR
#=======================================================================================
# 👉 Get Walls
wallsToCopy = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Walls)\
    .WhereElementIsNotElementType()\
    .ToElementIds()

#📐 Vector
vector = XYZ(50, 50, 0)

#🔓 Start Transaction
t = Transaction(doc, __title__)
t.Start()

#✅ Copy Elements
ElementTransformUtils.CopyElements(doc, wallsToCopy, vector)

#🔒 End Transaction
t.Commit()


#🟡 ╔═╗╔═╗╔═╗╦ ╦  ╔╗ ╔═╗╔╦╗╦ ╦╔═╗╔═╗╔╗╔  ╦  ╦╦╔═╗╦ ╦╔═╗
#🟡 ║  ║ ║╠═╝╚╦╝  ╠╩╗║╣  ║ ║║║║╣ ║╣ ║║║  ╚╗╔╝║║╣ ║║║╚═╗
#🟡 ╚═╝╚═╝╩   ╩   ╚═╝╚═╝ ╩ ╚╩╝╚═╝╚═╝╝╚╝   ╚╝ ╩╚═╝╚╩╝╚═╝ COPY BETWEEN VIEWS
#=======================================================================================

#👉 Get TextNotes
textToCopy = FilteredElementCollector(doc, doc.ActiveView.Id)\
    .OfCategory(BuiltInCategory.OST_TextNotes)\
    .WhereElementIsNotElementType()\
    .ToElementIds()

#👁️ ️Get Views
src_view = doc.ActiveView
dest_view = select_views(__title__,multiple=False)

#⚙ Transform & Options
transform = Transform.Identity
opts      = CopyPasteOptions()

#🔓 Start Transaction
t = Transaction(doc, __title__)
t.Start()

#✅ Copy Elements
ElementTransformUtils.CopyElements(src_view, textToCopy, dest_view, transform, opts)

#🔒 End Transaction
t.Commit()


#🟠 ╔═╗╔═╗╔═╗╦ ╦  ╔╗ ╔═╗╔╦╗╦ ╦╔═╗╔═╗╔╗╔  ╔═╗╦═╗╔═╗ ╦╔═╗╔═╗╔╦╗╔═╗
#🟠 ║  ║ ║╠═╝╚╦╝  ╠╩╗║╣  ║ ║║║║╣ ║╣ ║║║  ╠═╝╠╦╝║ ║ ║║╣ ║   ║ ╚═╗
#🟠 ╚═╝╚═╝╩   ╩   ╚═╝╚═╝ ╩ ╚╩╝╚═╝╚═╝╝╚╝  ╩  ╩╚═╚═╝╚╝╚═╝╚═╝ ╩ ╚═╝ COPY BETWEEN PROJECTS
#=======================================================================================
# 👉 Get Walls
wallsToCopy = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Walls)\
    .WhereElementIsNotElementType()\
    .ToElementIds()


#🏠 Get all Docs
all_docs = list(app.Documents)
doc_A = all_docs[0]
doc_B = all_docs[1]


#⚙ Transform & Options
transform = Transform.Identity
opts      = CopyPasteOptions()

#🔓 Start Transaction
t = Transaction(doc_B, __title__)
t.Start()

#✅ Copy Elements
ElementTransformUtils.CopyElements(doc_A, wallsToCopy, doc_B, transform, opts)

#🔒 End Transaction
t.Commit()

