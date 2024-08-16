#!python3
__title__ = "7 - Install More Python Packages"
__doc__ = """Version = 1.0
Date    = 24.06.2024
_____________________________________________________________________
Description:
Learn how to use more python3 packages in pyRevit like:
numpy, pandas, openpyxl and many more!
_____________________________________________________________________
Author: Erik Frits from LearnRevitAPI.com"""

#_____________________________________________________________________
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝


# # # Check python version
import sys
print("Python version:", sys.version)
# print("Version info:", sys.version_info)

import sys
sys.path.append(r'C:\Users\Lenny 16 Inch\AppData\Local\Programs\Python\Python38\Lib\site-packages')
sys.path.append(r'C:\Users\Lenny 16 Inch\AppData\Local\Programs\Python\Python38\Lib')
sys.path.append(r'C:\\Users\\Lenny 16 Inch\\AppData\\Local\\Programs\\Python\\Python38\\DLLs')
sys.path.append(r'C:\\Users\\Lenny 16 Inch\\AppData\\Local\\Programs\\Python\\Python38')

# 'C:\\Users\\Lenny 16 Inch',
# 'C:\\Users\\Lenny 16 Inch\\AppData\\Local\\Programs\\Python\\Python38\\python38.zip',
# 'C:\\Users\\Lenny 16 Inch\\AppData\\Local\\Programs\\Python\\Python38\\DLLs',
# 'C:\\Users\\Lenny 16 Inch\\AppData\\Local\\Programs\\Python\\Python38\\lib',
# 'C:\\Users\\Lenny 16 Inch\\AppData\\Local\\Programs\\Python\\Python38',
# 'C:\\Users\\Lenny 16 Inch\\AppData\\Local\\Programs\\Python\\Python38\\lib\\site-packages',




#_____________________________________________________________________
#🟧 Numpy
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(arr)
print(type(arr))

#_____________________________________________________________________
#🟧 PANDAS
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
print(df)
#_____________________________________________________________________
#🟧 OPENPYXL
from openpyxl import Workbook

wb = Workbook()
print(wb)

#_____________________________________________________________________
#🟧 Autodesk
from Autodesk.Revit.DB import *
doc    = __revit__.ActiveUIDocument.Document #type:Document


walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()
print(walls)



