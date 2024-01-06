# -*- coding: utf-8 -*-
__title__ = 'What is Revit API?'

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#--------------------------------------------------
from Autodesk.Revit.DB import *

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#--------------------------------------------------
document = __revit__.ActiveUIDocument.Document
viewId   = document.ActiveView.Id
position = XYZ(0,0,0)
text     = 'Visit LearnRevitAPI.com to Learn More!'
typeId   = document.GetDefaultElementTypeId(ElementTypeGroup.TextNoteType)

t = Transaction(document, 'Create TextNote')
t.Start()
TextNote.Create(document, viewId, position, text, typeId)
t.Commit()



























