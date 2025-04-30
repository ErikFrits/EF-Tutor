# -*- coding: utf-8 -*-
__title__   = "09 - Add SharedParams"
__doc__     = """Version = 1.0
Date    = 04.12.2024
________________________________________________________________
Description:


________________________________________________________________
Author: Erik Frits"""

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================
#⬇️ Imports
from Autodesk.Revit.DB import *


# 🍪 Variables
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# 📂 Access SharedParameterFile
sp_file = app.OpenSharedParameterFile()


# 🗂 Sort All Parameters from SharedParameterFile
dict_shared_params = {}
for group in sp_file.Groups:
    for p_def in group.Definitions:
        combined_name = '[{}]_{}'.format(group.Name, p_def.Name)
        dict_shared_params[combined_name] = p_def


#1️⃣ Use pyRevit Forms to choose SharedParameters
from pyrevit import forms
selected_p_names = forms.SelectFromList.show(
    sorted(dict_shared_params.keys()),
    button_name='Select Parameters',
    multiselect=True)
selected_param_defs = [dict_shared_params[p_name] for p_name in selected_p_names]

# 📊 Print Selected Parameters
#print(selected_p_names)
#print(selected_param_defs)



#2️⃣ Select Categories and create CategorySet
cat_set = app.Create.NewCategorySet()
cat_view = Category.GetCategory(doc, BuiltInCategory.OST_Views)
cat_set.Insert(cat_view)

#3️⃣ Create Instance Binding
new_instance_binding = app.Create.NewInstanceBinding(cat_set)
#new_type_binding    = app.Create.NewTypeBinding(cat_set)

#4️⃣ Select Parameter Group
parameter_group = BuiltInParameterGroup.PG_ANALYSIS_RESULTS

#5️⃣ Add Parameters
t = Transaction(doc, 'Add Shared Parameters')
t.Start() #🔓 Start Transaction

# Iterate through ParameterGroups and ParameterDefinitions
for p_def in selected_param_defs:
    try:
        doc.ParameterBindings.Insert(p_def,
                                     new_instance_binding,
                                     parameter_group)

        print('✅Added Parameter: {}'.format(p_def.Name))
    except:
         print('❌Failed to add {}'.format(p_def.Name))



t.Commit()#🔒 Commit Transaction

