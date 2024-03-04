# -*- coding: utf-8 -*-
__title__   = "05 - Create/Delete/Copy Elements"
__author__  = "Erik Frits"
__version__ = "Version 1.0"
__doc__ = """Version = 1.0
Date    = 18.09.2022
_____________________________________________________________________
Description:
Code from YouTube tutorial about Creating/Deleting/Copying Elements
using Revit API.  
_____________________________________________________________________
Author:  Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#====================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import StructuralType

#.NET IMPORTS
import clr
clr.AddReference('System')
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#====================================================================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

active_view  = doc.ActiveView
active_level = doc.ActiveView.GenLevel

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#====================================================================================================
with Transaction(doc,__title__) as t:
    t.Start()
    #CHANGES HERE


    # ╔╦╗╔═╗═╗ ╦╔╦╗
    #  ║ ║╣ ╔╩╦╝ ║
    #  ╩ ╚═╝╩ ╚═ ╩ TEXT
    # ==================================================
    # ARGUMENTS
    # text_type_id = FilteredElementCollector(doc).OfClass(TextNoteType).FirstElementId()
    # pt           = XYZ(0,0,0)
    # text         = 'Hello BIM World!'
    # # CREATE TEXT NOTE
    # TextNote.Create(doc, active_view.Id, pt, text, text_type_id)

    # ╦═╗╔═╗╔═╗╔╦╗
    # ╠╦╝║ ║║ ║║║║
    # ╩╚═╚═╝╚═╝╩ ╩ ROOM
    #==================================================
    # # ARGUMENTS
    # pt = UV(10,0)
    #
    # # CREATE ROOM
    # room = doc.Create.NewRoom(active_level, pt)
    #
    # # CREATE ROOM TAG
    # room_link = LinkElementId(room.Id)
    # doc.Create.NewRoomTag(room_link, pt, active_view.Id )

    # ╦  ╦╔╗╔╔═╗╔═╗
    # ║  ║║║║║╣ ╚═╗
    # ╩═╝╩╝╚╝╚═╝╚═╝ DETAIL LINES
    # ==================================================
    # ARGUMENTS
    # pt_start = XYZ(20,0,0)
    # pt_end   = XYZ(20,5,0)
    # curve    = Line.CreateBound(pt_start, pt_end)
    #
    # CREATE DETAIL LINE
    # detail_line = doc.Create.NewDetailCurve(active_view, curve)

    # ╦ ╦╔═╗╦  ╦  ╔═╗
    # ║║║╠═╣║  ║  ╚═╗
    # ╚╩╝╩ ╩╩═╝╩═╝╚═╝ WALLS
    #==================================================
    # # ARGUMENTS
    # pt_start = XYZ(30,0,0)
    # pt_end   = XYZ(30,5,0)
    # curve    = Line.CreateBound(pt_start, pt_end)
    #
    # # CREATE A WALL
    # wall = Wall.Create(doc, curve, active_level.Id, False)

    # ╦ ╦╦╔╗╔╔╦╗╔═╗╦ ╦╔═╗
    # ║║║║║║║ ║║║ ║║║║╚═╗
    # ╚╩╝╩╝╚╝═╩╝╚═╝╚╩╝╚═╝ WINDOWS
    #==================================================
    # # ARGUMENTS
    # host_wall = doc.GetElement(ElementId(779500))
    # pt_start = XYZ(30,0,0)
    # pt_end   = XYZ(30,5,0)
    # pt_mid   = (pt_start + pt_end) /2
    # window_type = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows)\
    #                 .WhereElementIsElementType().FirstElement()
    #
    # # CREATE A WINDOW
    # window = doc.Create.NewFamilyInstance(pt_mid, window_type, host_wall, StructuralType.NonStructural )

    # ╔═╗╔═╗╔╦╗╦╦ ╦ ╦  ╦╔╗╔╔═╗╔╦╗╔═╗╔╗╔╔═╗╔═╗
    # ╠╣ ╠═╣║║║║║ ╚╦╝  ║║║║╚═╗ ║ ╠═╣║║║║  ║╣
    # ╚  ╩ ╩╩ ╩╩╩═╝╩   ╩╝╚╝╚═╝ ╩ ╩ ╩╝╚╝╚═╝╚═╝ FAMILY INSTANCE
    #==================================================
    # # EXTRA FUNCTION
    # def get_type_by_name(type_name):
    #     """Extra Function to get Family Type by name."""
    #     # CREATE RULE
    #     param_type = ElementId(BuiltInParameter.ALL_MODEL_TYPE_NAME)
    #     f_param    = ParameterValueProvider(param_type)
    #     evaluator  = FilterStringEquals()
    #     f_rule     = FilterStringRule(f_param, evaluator, type_name, True) # Revit 2023 does not need last argument!
    #
    #     # CREATE FILTER
    #     filter_type_name = ElementParameterFilter(f_rule)
    #
    #     # GET ELEMENTS
    #     return FilteredElementCollector(doc).WherePasses(filter_type_name).WhereElementIsElementType().FirstElement()
    #
    # # ARGUMENTS
    # pt = XYZ(40,5,0)
    # symbol = get_type_by_name('Placeholder - Type B')
    #
    # # CREATE AN ELEMENT
    # element = doc.Create.NewFamilyInstance(pt, symbol, StructuralType.NonStructural)


    # ╔═╗╦ ╦╔═╗╔═╗╔╦╗╔═╗
    # ╚═╗╠═╣║╣ ║╣  ║ ╚═╗
    # ╚═╝╩ ╩╚═╝╚═╝ ╩ ╚═╝ SHEETS
    #==================================================
    # # ARGUMENTS
    # title_block_id = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks)\
    #                     .WhereElementIsNotElementType().FirstElementId()
    #
    # # CREATE SHEET
    # new_sheet = ViewSheet.Create(doc, title_block_id)
    # new_sheet.SheetNumber = 'Random Sheet Number' #<- Unique !
    # new_sheet.Name        = 'Random Name'

    # ╦  ╦╦╔═╗╦ ╦╔═╗
    # ╚╗╔╝║║╣ ║║║╚═╗
    #  ╚╝ ╩╚═╝╚╩╝╚═╝ VIEWS
    #==================================================
    # # ARGUMENTS
    # all_view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
    # view_3D_type = [vt for vt in all_view_types if vt.ViewFamily == ViewFamily.ThreeDimensional][0]
    #
    # # CREATE 3D VIEW
    # new_3D = View3D.CreateIsometric(doc, view_3D_type.Id)

    # ╦═╗╔═╗╔═╗╦╔═╗╔╗╔
    # ╠╦╝║╣ ║ ╦║║ ║║║║
    # ╩╚═╚═╝╚═╝╩╚═╝╝╚╝ REGION
    #==================================================
    # # ARGUMENTS
    # region_type_id = doc.GetDefaultElementTypeId(ElementTypeGroup.FilledRegionType)
    #
    # # POINTS
    # pt_0 = XYZ(50, 0, 0)
    # pt_1 = XYZ(55, 0, 0)
    # pt_2 = XYZ(55, 5, 0)
    # pt_3 = XYZ(50, 5, 0)
    #
    # # LINES
    # l_0 = Line.CreateBound(pt_0, pt_1)
    # l_1 = Line.CreateBound(pt_1, pt_2)
    # l_2 = Line.CreateBound(pt_2, pt_3)
    # l_3 = Line.CreateBound(pt_3, pt_0)
    #
    # # BOUNDARY
    # boundary = CurveLoop()
    # boundary.Append(l_0)
    # boundary.Append(l_1)
    # boundary.Append(l_2)
    # boundary.Append(l_3)
    #
    # # LIST OF BOUNDARIES
    # list_boundaries = List[CurveLoop]()
    # list_boundaries.Add(boundary)
    #
    # # CREATE FILLED REGION
    # region = FilledRegion.Create(doc, region_type_id, active_view.Id, list_boundaries)

    # ╔═╗╦  ╔═╗╔═╗╦═╗
    # ╠╣ ║  ║ ║║ ║╠╦╝
    # ╚  ╩═╝╚═╝╚═╝╩╚═ FLOOR
    #==================================================
    # # ARGUMENTS
    # floor_type_id = doc.GetDefaultElementTypeId(ElementTypeGroup.FloorType)
    # floor_type    = doc.GetElement(floor_type_id)
    #
    # # POINTS
    # pt_0 = XYZ(60, 0, 0)
    # pt_1 = XYZ(65, 0, 0)
    # pt_2 = XYZ(65, 5, 0)
    # pt_3 = XYZ(60, 5, 0)
    #
    # # LINES
    # l_0 = Line.CreateBound(pt_0, pt_1)
    # l_1 = Line.CreateBound(pt_1, pt_2)
    # l_2 = Line.CreateBound(pt_2, pt_3)
    # l_3 = Line.CreateBound(pt_3, pt_0)
    #
    # # BOUNDARY
    # boundary = CurveArray()
    # boundary.Append(l_0)
    # boundary.Append(l_1)
    # boundary.Append(l_2)
    # boundary.Append(l_3)
    #
    # # CREATE FLOOR
    # new_floor = doc.Create.NewFloor(boundary, floor_type, active_level, False)

    # ╔═╗╔═╗╔═╗╦ ╦  ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗
    # ║  ║ ║╠═╝╚╦╝  ║╣ ║  ║╣ ║║║║╣ ║║║ ║ ╚═╗
    # ╚═╝╚═╝╩   ╩   ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝ COPY ELEMENTS
    # ==================================================
    # # GET ELEMENTS TO COPY
    # all_floors_in_view = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElementIds()
    # elements_to_copy = List[ElementId](all_floors_in_view)
    #
    # # COPY ELEMENTS (Multiple Times)
    # for i in range(1,6):
    #     vector = XYZ(2*i, 10*i, 0)
    #     ElementTransformUtils.CopyElements(doc, elements_to_copy, vector)

    # ╔╦╗╔═╗╦  ╔═╗╔╦╗╔═╗  ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗
    #  ║║║╣ ║  ║╣  ║ ║╣   ║╣ ║  ║╣ ║║║║╣ ║║║ ║ ╚═╗
    # ═╩╝╚═╝╩═╝╚═╝ ╩ ╚═╝  ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝ DELETE ELEMENTS
    # ==================================================
    # # # GET ELEMENTS TO COPY
    # all_floors_in_view = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElementIds()
    # element_to_delete  = List[ElementId](all_floors_in_view)
    #
    # # DELETE ELEMENTS
    # doc.Delete(element_to_delete)

    t.Commit()





#⬇ IMPORTS
from Autodesk.Revit.DB import *



#📦 VARIABLES
doc          = __revit__.ActiveUIDocument.Document
active_view  = doc.ActiveView
active_level = doc.ActiveView.GenLevel

#🎴 ALL VIEW TYPES
view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

#🔎 FILTER CERTAIN VIEW TYPES
view_types_plans      = [vt for vt in view_types if vt.ViewFamily == ViewFamily.FloorPlan]
view_types_sections   = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Section]
view_types_3D         = [vt for vt in view_types if vt.ViewFamily == ViewFamily.ThreeDimensional]
view_types_legends    = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Legend]
view_types_drafting   = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Drafting]
view_types_elevations = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Elevation]
view_types_ceil_views = [vt for vt in view_types if vt.ViewFamily == ViewFamily.CeilingPlan]
view_types_structural = [vt for vt in view_types if vt.ViewFamily == ViewFamily.StructuralPlan]
view_types_area       = [vt for vt in view_types if vt.ViewFamily == ViewFamily.AreaPlan]
view_types_sheet      = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Sheet]




def create_element_section(curve, origin, H=5,W=5,D=5, offset =0):
    #type:(Curve, XYZ, float,float,float,float) -> ViewSection
    """This function will generate a ViewSection with a special crop.
    :param curve:   Curve for taking vector of orientation of the section.
    :param origin:  XYZ Point from where all dimensions will be taken
    :param H:       Height
    :param W:       Width
    :param D:       Depth
    :param offset:  Offset from H,W,D to make a little more space
    :return:        generated ViewSection"""
    Thanks_to = """Thanks to martin.marek for his Snippet. It saved me a lot of time!
    https://forum.dynamobim.com/t/create-section-view-of-the-wall-by-python/44986/6"""

    pt_start = curve.GetEndPoint(0)
    pt_end   = curve.GetEndPoint(1)
    vector   = pt_end - pt_start


    # SECTION - DIRECTION
    fc = -1
    if pt_start.X > pt_end.X or (pt_start.X == pt_end.X and pt_start.Y < pt_end.Y):
        fc = 1

    # SECTION - ORIENTATION
    curvedir = fc * vector.Normalize()

    t        = Transform.Identity
    t.Origin = origin
    t.BasisX = curvedir
    t.BasisY = XYZ.BasisZ
    t.BasisZ = curvedir.CrossProduct(XYZ.BasisZ)

    # SECTION - CROPBOX
    sectionBox           = BoundingBoxXYZ()
    sectionBox.Transform = t                            #apply orientation
    sectionBox.Min       = XYZ(W*-0.5 -offset, 0 -offset, D*-0.5 -offset)
    sectionBox.Max       = XYZ(W* 0.5 +offset, H +offset, D* 0.5 +offset)

    # SECTION - VIEWTYPE
    view_types    = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
    SC_view_types = [v for v in view_types if v.ViewFamily == ViewFamily.Section]
    SC_Type       = SC_view_types[0]

    # CREATE SECTION
    view_section = ViewSection.CreateSection(doc, SC_Type.Id, sectionBox)

    # ACTIVATE CROP
    view_section.get_Parameter(BuiltInParameter.VIEWER_CROP_REGION).Set(1)

    return view_section
