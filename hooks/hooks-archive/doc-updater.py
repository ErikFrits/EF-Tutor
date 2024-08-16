# -*- coding: utf-8 -*-

#⬇️ Imports
from datetime import datetime
from Autodesk.Revit.DB import (BuiltInCategory,
                               BuiltInParameter,
                               UnitUtils,
                               UnitTypeId,
                               ElementId,
                               WorksharingUtils,
                               FamilyInstance)

#📦 Variables
sender = __eventsender__
args   = __eventargs__

doc = args.GetDocument()

#👉 Get ElementIds for Modified/Deleted/New
modified_el_ids = args.GetModifiedElementIds()
deleted_el_ids  = args.GetDeletedElementIds()
new_el_ids      = args.GetAddedElementIds()

modified_el = [doc.GetElement(e_id) for e_id in modified_el_ids]



#🎯 IUpdater - Modified Elements
allowed_cats = [ElementId(BuiltInCategory.OST_Windows), ElementId(BuiltInCategory.OST_Doors)]
for el in modified_el:
    if type(el) != FamilyInstance:
        continue

    if el.Category.Id in allowed_cats:

        try:

            #1️⃣ Update XYZ Coordinates in Meters
            p_com = el.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)

            pt    = el.Location.Point
            x = round(UnitUtils.ConvertFromInternalUnits(pt.X, UnitTypeId.Meters), 2)
            y = round(UnitUtils.ConvertFromInternalUnits(pt.Y, UnitTypeId.Meters), 2)
            z = round(UnitUtils.ConvertFromInternalUnits(pt.Z, UnitTypeId.Meters), 2)

            coord = "{}, {}, {}".format(x,y,z)
            p_com.Set(coord)


            #2️⃣ Add Timestamp to Edited Elements
            # Get Time and UserName
            timestamp = datetime.now()
            f_timestamp = timestamp.strftime("%Y-%m-%d %H-%M-%S")

            wti  = WorksharingUtils.GetWorksharingTooltipInfo(doc, el.Id)
            last = wti.LastChangedBy

            # Change Value
            value  = "{} (at {})".format(last, f_timestamp)
            p_last = el.LookupParameter('LastModifiedBy')
            if p_last:
                p_last.Set(value)


            #3️⃣ Update Mirror State
            value = 'Mirrored' if el.Mirrored else 'Not Mirrored'
            p_mirrored = el.LookupParameter('IsMirrored')

            if p_mirrored:
                p_mirrored.Set(value)

        except:
            #import traceback
            #print(traceback.format_exc())
            pass



