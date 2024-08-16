# -*- coding: utf-8 -*-
__title__   = "Tutorial Create Sections: Windows"
__doc__ = """Date    = 29.01.2024
_____________________________________________________________________
Description:
Create sections for all window types.
_____________________________________________________________________
Author: Erik Frits"""
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
from Autodesk.Revit.DB import *
from pyrevit import forms

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
uidoc     = __revit__.ActiveUIDocument
doc       = __revit__.ActiveUIDocument.Document #type: Document
app       = __revit__.Application


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
#==================================================


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================

#👉 Get Window Instances of Each Type
windows = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()
dict_windows = {Element.Name.GetValue(win.Symbol): win for win in windows if type(win.Host) == Wall} # Add Snippet on Screen explaining Comprehension

#👀 Preview Dict
# for k,v in dict_windows.items():
#     print(k,v)


#🔏 Create Transaction to Modify Project
t = Transaction(doc, 'Generate Window Sections')
t.Start() #🔓


#🎯 Create Sections
for type_name, window in dict_windows.items():
    try:

        #1️⃣ Get Window Origin Point
        win_origin = window.Location.Point      #type: XYZ

        #2️⃣ Calculate Vector based on Wall
        host_wall = window.Host
        curve     = host_wall.Location.Curve    #type: Curve
        pt_start  = curve.GetEndPoint(0)        #type: XYZ
        pt_end    = curve.GetEndPoint(1)        #type: XYZ
        vector    = pt_end - pt_start           #type: XYZ

        #3️⃣ Get Window Size
        try:
            win_height = window.Symbol.get_Parameter(BuiltInParameter.CASEWORK_HEIGHT).AsDouble() # Not all windows use it.
            if not win_height: # Alternative Height parameter
                win_height = window.Symbol.LookupParameter('Höhe ab FBOK').AsDouble()
        except:             pass
        win_width  = window.Symbol.get_Parameter(BuiltInParameter.GENERIC_WIDTH).AsDouble()
        offset     = UnitUtils.ConvertToInternalUnits(40, UnitTypeId.Centimeters) #40cm
        win_depth  = 2

        print(UnitUtils.ConvertFromInternalUnits(win_width, UnitTypeId.Centimeters))
        print(UnitUtils.ConvertFromInternalUnits(win_height, UnitTypeId.Centimeters))

        #4️⃣🅰️ Define Transform  (Location + Rotation)
        trans        = Transform.Identity # Create Instance of Transform
        trans.Origin = win_origin         # Set Origin Point


        #4️⃣🅱️ Set directions of X,Y,Z Axis of Transform
        vector = vector.Normalize() * -1 # Normalized indicates that the length of this vector equals one (a unit vector).

        #❇️ Create Elevation Transform
        trans.BasisX = vector
        trans.BasisY = XYZ.BasisZ
        trans.BasisZ = vector.CrossProduct(XYZ.BasisZ) #Sets the Z-axis to be perpendicular to both curvedir and the
                                                         # vertical axis (essentially pointing in or out of the wall).

        #
        # #❇️ Create Cross Section Transform
        # # Calculate Window's Normal Vector (Perpendicular to the Window Plane)
        # vector_cross = vector.CrossProduct(XYZ.BasisZ).Normalize()
        #
        # # Align BasisX or BasisY with the Window's Normal Vector
        # trans.BasisX = vector_cross  # Aligned with the window's normal
        # trans.BasisY = XYZ.BasisZ  # Vertical
        # trans.BasisZ = vector_cross.CrossProduct(XYZ.BasisZ)  # Perpendicular to both


        # #❇️ Create FloorPlan(Section) Transform
        #
        # # Assuming XYZ is a class with standard basis vectors and trans is your transformation object
        # vector = vector.Normalize()
        #
        # # Set Z-axis to global up direction (perpendicular to floor)
        # trans.BasisZ = XYZ.BasisZ
        #
        # # Set X-axis based on building's main direction or a default
        # trans.BasisX = vector
        #
        # # Calculate Y-axis as perpendicular to both X-axis and Z-axis
        # # Ensure it is normalized to maintain the unit vector property
        # trans.BasisY = trans.BasisZ.CrossProduct(trans.BasisX).Normalize()
        #
        # # Verify that all axes are perpendicular to each other
        # # If not, adjust mainDirection or use a different approach to calculate BasisX and BasisY



        #5️⃣ Create SectionBox (Add Dimensions + Apply Transform)
        section_box = BoundingBoxXYZ() #0,0,0
        half_w      = win_width/2
        section_box.Min = XYZ(-half_w - offset,    0          - offset,    -2)         # z - Depth Start
        section_box.Max = XYZ(half_w  + offset,    win_height + offset,    win_depth) # z - Depth End
        # 💡
        # X - Left/Right
        # Y - Up/Down
        # Z - Depth (Forward, Backwards)

        section_box.Transform = trans


        #6️⃣ Create Section View
        view_type_id   = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeSection) # Default Section Type
        window_section = ViewSection.CreateSection(doc, view_type_id, section_box)

        #7️⃣ Rename View
        win_family_name = window.Symbol.Family.Name
        win_type_name   = Element.Name.GetValue(window.Symbol)
        new_name        = "py_{}_{}".format(win_family_name, win_type_name)

        for i in range(10):
            try:
                window_section.Name = new_name
                print(window.Id, new_name)
                break
            except:
                new_name += '*'
    except:
        import traceback
        print('---\nERROR:')
        print(traceback.format_exc())

t.Commit() #🔒



uidoc.ActiveView = window_section