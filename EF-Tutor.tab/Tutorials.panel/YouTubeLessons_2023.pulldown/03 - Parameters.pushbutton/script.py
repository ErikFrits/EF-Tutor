# -*- coding: utf-8 -*-
__title__ = "03 - RevitAPI: Parameters"
__doc__ = """This script is part of YouTube video
where I explain RevitAPI Parameters and how to work with them.

You can support my channel on:
www.patreon.com/ErikFrits"""
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

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
# print("*** It's time to learn how to use Parameters with RevitAPI + python. ***")

# ╔═╗╔═╗╔╦╗  ╦ ╦╔═╗╦  ╦
# ║ ╦║╣  ║   ║║║╠═╣║  ║
# ╚═╝╚═╝ ╩   ╚╩╝╩ ╩╩═╝╩═╝ GET A WALL
#====================================================================================================
wall_id = ElementId(428745)
wall    = doc.GetElement(wall_id)
# print(wall)
# print(list(wall.Parameters))

# ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗╔═╗
# ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝╚═╗
# ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═╚═╝ PARAMETERS
#====================================================================================================
# print('*'*100)
# print('*** Parameters: ***')
# for p in wall.Parameters:
    # if p.Definition.Name == 'Comments':    # DON'T USE THIS METHOD
    #     print("It's a comment parmaeter!")
    #     print(p.Id)

    # print(p)
    # print('.Name:             {}'.format(p.Definition.Name))
    # print('.BuiltInParameter: {}'.format(p.Definition.BuiltInParameter))
    # print('.StorageType:      {}'.format(p.StorageType))
    # print('.IsShared:         {}'.format(p.IsShared))
    # print('.IsReadOnly:       {}'.format(p.IsReadOnly))
    # print("-"*50)

# ╔═╗╔═╗╔╦╗  ╔╗ ╦ ╦╦╦ ╔╦╗  ╦╔╗╔  ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗
# ║ ╦║╣  ║   ╠╩╗║ ║║║  ║───║║║║  ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝
# ╚═╝╚═╝ ╩   ╚═╝╚═╝╩╩═╝╩   ╩╝╚╝  ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═ GET BUILT-IN PARAMETER
# ====================================================================================================
# print('-' * 100)
# print('*** Built-in Parameters: ***')
# wall_comments  = wall.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
# wall_type_name = wall.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()
#
# print('.Name:             {}'.format(wall_comments.Definition.Name))
# print('.BuiltInParameter: {}'.format(wall_comments.Definition.BuiltInParameter))
# print('.StorageType:      {}'.format(wall_comments.StorageType))
# print('.IsShared:         {}'.format(wall_comments.IsShared))
# print('.IsReadOnly:       {}'.format(wall_comments.IsReadOnly))
# print("-"*50)
#
# print(wall_comments.AsString())

# ╔═╗╔═╗╔╦╗  ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗  ╔╗ ╦ ╦  ╔╗╔╔═╗╔╦╗╔═╗
# ║ ╦║╣  ║   ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝  ╠╩╗╚╦╝  ║║║╠═╣║║║║╣
# ╚═╝╚═╝ ╩   ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═  ╚═╝ ╩   ╝╚╝╩ ╩╩ ╩╚═╝ GET PARAMETER BY NAME
#====================================================================================================
# print('*** Getting Shared Parameters: ***')

# GET PROJECT/SHARED PARAMETER
# sp_text = wall.LookupParameter('sp_text')
# print(sp_text.AsString())

# sp_mat_id = wall.LookupParameter('sp_material').AsElementId()
# sp_mat = doc.GetElement(sp_mat_id)
# print(sp_mat)
# print(sp_mat.Name)

# sp_text = wall.LookupParameter('sp_bool')
# print(sp_text.AsInteger())



# ╔═╗╔═╗╔╦╗  ╔╦╗╦ ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗╔═╗
# ║ ╦║╣  ║    ║ ╚╦╝╠═╝║╣   ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝╚═╗
# ╚═╝╚═╝ ╩    ╩  ╩ ╩  ╚═╝  ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═╚═╝ GET TYPE PARMAETERS
#====================================================================================================
# print('-'*100)
# print("*** GET TYPE PARAMETERS ***")
#
# wall_type = wall.WallType
# wall_type_description = wall_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION)
# wall_type_mark        = wall_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_MARK)
# print(wall_type_description.AsString())
# print(wall_type_mark.AsString())

# ╔═╗╔═╗╔╦╗  ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗  ╦  ╦╔═╗╦  ╦ ╦╔═╗
# ╚═╗║╣  ║   ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝  ╚╗╔╝╠═╣║  ║ ║║╣
# ╚═╝╚═╝ ╩   ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═   ╚╝ ╩ ╩╩═╝╚═╝╚═╝ SET PARAMETER VALUE
#====================================================================================================
# GET PARAMETERS
# wall_comments = wall.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
# sp_area       = wall.LookupParameter('sp_area')
# sp_bool       = wall.LookupParameter('sp_bool')
# sp_float      = wall.LookupParameter('sp_float')
# sp_int        = wall.LookupParameter('sp_int')
# sp_length     = wall.LookupParameter('sp_length')
# sp_mat        = wall.LookupParameter('sp_material')
# sp_text       = wall.LookupParameter('sp_text')

# SET PARAMTERES
# t = Transaction(doc, __title__)
# t.Start()

# # wall_comments.Set('That was terrible joke. Comment better jokes under my video.')
# # print(wall_comments.AsString())

# sp_area.Set(555.55)
# sp_bool.Set(1)
# sp_float.Set(25.5)
# sp_int.Set(100)
# sp_length.Set(99.99)
# new_mat_id = ElementId(414)
# sp_mat.Set(new_mat_id)
# sp_text.Set(str(1000))
# print('Setting parameters is complete.')
# t.Commit()

# ╔═╗╦  ╔═╗╔╗ ╔═╗╦    ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗╔═╗
# ║ ╦║  ║ ║╠╩╗╠═╣║    ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝╚═╗
# ╚═╝╩═╝╚═╝╚═╝╩ ╩╩═╝  ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═╚═╝ GLOBAL PARAMETERS
#====================================================================================================
# print('*** GLOBAL PARAMETERS ***')

# GET ALL GLOBAL PARAMETERS
# all_global_parameter_ids = GlobalParametersManager.GetAllGlobalParameters(doc)
#
# t = Transaction(doc,'Changing Global Parameters')
# t.Start()

# PRINT GLOBAL PARAMETERS DATA
# for p_id in all_global_parameter_ids:
    # p = doc.GetElement(p_id)
    # print('Name:          {}'.format(p.Name))
    # print('GetDefinition: {}'.format(p.GetDefinition()))
    # print('GetFormula:    {}'.format(p.GetFormula()))
    # print('GetValue:      {}'.format(p.GetValue().Value))
    # print('-'*50)

    # CHANGE GLOBAL PARAMETER VALUE OR FORMULA
    # new_value = StringParameterValue('New Value')
    # p.SetValue(new_value)
    # p.SetFormula('"New Formula"')


# t.Commit()

# ╔═╗╦ ╦╔═╗╔╦╗╔═╗╔╦╗  ╔╦╗╔═╗╔═╗╦
# ║  ║ ║╚═╗ ║ ║ ║║║║   ║ ║ ║║ ║║
# ╚═╝╚═╝╚═╝ ╩ ╚═╝╩ ╩   ╩ ╚═╝╚═╝╩═╝
#====================================================================================================

t = Transaction(doc,'Writing ElementIds to Mark parameter of Walls.')
t.Start()

# SET WALL ELEMENT-ID TO MARK
all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

for wall in all_walls:
    wall_mark = wall.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
    wall_mark.Set(str(wall.Id))
    print(wall.Id)
t.Commit()

print('The script is complete. Comment ⌨ emoji in the comments if you following along.')





