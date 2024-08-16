# -*- coding: utf-8 -*-
__title__   = "2 - Automate Views on Sheets"
__doc__ = """Date    = 12.02.2024
_____________________________________________________________________
Description:
Tutorials on how to Place Views on New Sheets.
_____________________________________________________________________
Author: Erik Frits"""
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc       = __revit__.ActiveUIDocument.Document #type: Document

# Global
default_title_block_id = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_TitleBlocks))


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================

# 📦 Get All Views + Filter
all_views      = FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType().ToElements()
views_to_place = [view for view in all_views if 'py_' in view.Name]

# ♻️ Sort Views for Placing on Sheets
from collections import defaultdict
dict_views = defaultdict(dict)

#🎯 Desired Dict Structure
# dict_views = {'VIEW_NAME' : {'Plan': None,
#                              'Elevation': None,
#                              'Cross': None},
#               }

# 👇 Sort Views to Place
for view in views_to_place:
    try:
        view_name = view.Name.replace('py_', '') #Remove py_ prefix
        win_name  = view_name.split(' (')[0]

        if   '(Plan)'      in view.Name: dict_views[win_name]['Plan']      = view
        elif '(Cross)'     in view.Name: dict_views[win_name]['Cross']     = view
        elif '(Elevation)' in view.Name: dict_views[win_name]['Elevation'] = view

    except:
        pass

#👀 Preview Results
# for win_name, dict_win_views in dict_views.items():
#     print(win_name)
#     for view in dict_win_views.values():
#         print('- {}'.format(view.Name))
#     print('-'*50)


#🔏 Transaction to Make changes
t = Transaction(doc, 'Create Window Sheets')
t.Start() #🔓



# 📰 Iterate and Create New Sheet
counter = 0
for win_name, dict_win_views in dict_views.items():
    #🪟 Get Plan/Cross/Elevation Views
    plan = dict_win_views['Plan']
    elev = dict_win_views['Elevation']
    cros = dict_win_views['Cross']

    # ⚠️ Handle Errors during view placement (SubTransaction)
    # SubTransaction Will allow creation of new Section only if we can place them
    # Otherwise this step will be rollbacked for this iteration
    st = SubTransaction(doc)
    st.Start()


    #📰 Create new ViewSheet
    new_sheet = ViewSheet.Create(doc, default_title_block_id)

    #💡 Check if possible to place views
    if Viewport.CanAddViewToSheet(doc, new_sheet.Id, plan.Id) and \
    Viewport.CanAddViewToSheet(doc, new_sheet.Id, elev.Id) and \
    Viewport.CanAddViewToSheet(doc, new_sheet.Id, cros.Id):
        st.Commit()
    else:
        st.RollBack()
        print('❌ The following window sections already placed: {}'.format(win_name))
        continue

    # ⏺️ Define position for placing views
    pt_plan = XYZ(-0.4,  0.3, 0)
    pt_cros = XYZ(-0.15, 0.75, 0)
    pt_elev = XYZ(-0.4,  0.75, 0)

    # 🖼️ Place Views on Sheets
    vp_plan = Viewport.Create(doc, new_sheet.Id, plan.Id, pt_plan)
    vp_cros = Viewport.Create(doc, new_sheet.Id, cros.Id, pt_cros)
    vp_elev = Viewport.Create(doc, new_sheet.Id, elev.Id, pt_elev)
    print('✅ Created New Sheet for Window: {}'.format(win_name))

    # 📝 Rename Sheets
    try:
        new_sheet.SheetNumber = 'Window - {}'.format(win_name)
        new_sheet.Name        = ''
    except:
        pass

    # # 📛️ Temp Counter
    # counter +=1
    # if counter > 10:
    #     break


t.Commit() #🔒





# 🎯 And this will create Hundreds of New Sheets for our Window Sections!