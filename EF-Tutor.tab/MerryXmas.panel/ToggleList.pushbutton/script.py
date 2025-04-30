#-*- coding: utf-8 -*-
__title__   = "Toggle SheetVisibility Menu"
__doc__     = """Version = 1.0
Date    = 13.02.2025
________________________________________________________________
Description:
Create a UI form to control the toggle state of ViewSheet parameter:  'Appears in Sheet List'.

It's quick and dirty prototype 🧙‍♂️. 
________________________________________________________________
Author: Erik Frits"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#====================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms   # By importing forms you also get references to WPF package! IT'S Very IMPORTANT !!!
import wpf, os, clr         # wpf can be imported only after pyrevit.forms!
from pyrevit.forms import select_views

# .NET Imports
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import Application, Window, Visibility
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem, TextBlock
from System import Uri

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
doc     = __revit__.ActiveUIDocument.Document #type: Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application

# Global Variables
# all_views  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
# dict_views = {'[{}]_{}'.format(view.ViewType,view.Name) : view for view in all_views}


# ╔╦╗╔═╗╦╔╗╔  ╔═╗╔═╗╦═╗╔╦╗
# ║║║╠═╣║║║║  ╠╣ ║ ║╠╦╝║║║
# ╩ ╩╩ ╩╩╝╚╝  ╚  ╚═╝╩╚═╩ ╩ MAIN FORM
#====================================================================================================
# Inherit .NET Window for your UI Form Class
class WPF_SheetToggle(Window):
    def __init__(self):
        # Connect to .xaml File (in the same folder!)
        path_xaml_file = os.path.join(PATH_SCRIPT, 'ListBoxSearch.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        # Populate Listbox with Views
        self.populate_listbox()

        # Show Form
        self.ShowDialog()



    # ╔╦╗╔═╗╔╦╗╦ ╦╔═╗╔╦╗╔═╗
    # ║║║║╣  ║ ╠═╣║ ║ ║║╚═╗
    # ╩ ╩╚═╝ ╩ ╩ ╩╚═╝═╩╝╚═╝ METHODS
    def populate_listbox(self):
        """Add Sheet items to your ListBox."""
        # Clear ListBox
        self.UI_listbox.Items.Clear()

        # Get Sheets
        all_sheets  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
        dict_sheets = {'[{}]_{}'.format(sheet.SheetNumber, sheet.Name): sheet for sheet in all_sheets}

        # Add ViewNames as CheckBoxes to ListBox
        for sheet_name, sheet in dict_sheets.items():
            self.create_listbox_item(sheet_name, sheet)



    def create_listbox_item(self, sheet_name, sheet):
        """Create ListBoxItem for each sheet"""

        # Create TextBlock to avoid error with '_'
        textblock = TextBlock()
        textblock.Text = sheet_name

        # Create CheckBox And add textblock to it
        checkbox = CheckBox()
        checkbox.Content = textblock
        checkbox.Tag = sheet  # You save your sheet to CheckBox.Tag parameter to access in other places...
        checkbox.Click += self.UIe_toggle_visibility  # assign event handler

        # Set Current Toggle State
        current_toggle = sheet.get_Parameter(BuiltInParameter.SHEET_SCHEDULED).AsInteger()
        checkbox.IsChecked = bool(current_toggle)

        # Add Checkbox to ListBoxItem
        listbox_item = ListBoxItem()
        listbox_item.Content = checkbox

        # PS You have a hierarchy ListBoxItem -> CheckBox -> TextBlock (it's important later if you need to modify it)

        # Add ListBoxItem to ListBox
        self.UI_listbox.Items.Add(listbox_item)




    # ╔╗ ╦ ╦╔╦╗╔╦╗╔═╗╔╗╔  ╔═╗╦  ╦╔═╗╔╗╔╔╦╗╔═╗
    # ╠╩╗║ ║ ║  ║ ║ ║║║║  ║╣ ╚╗╔╝║╣ ║║║ ║ ╚═╗
    # ╚═╝╚═╝ ╩  ╩ ╚═╝╝╚╝  ╚═╝ ╚╝ ╚═╝╝╚╝ ╩ ╚═╝
    def UIe_btn_run(self, sender, e):
        print('Form Submitted!')
        self.Close()


    def UIe_search_text_changed(self, sender, e):
        search_text = self.UI_search.Text.lower()

        if search_text:
            search_words = search_text.split()

            for listbox_item in self.UI_listbox.Items:
                checkbox  = listbox_item.Content
                textblock = checkbox.Content
                view_name = textblock.Text.lower()

                if all(word in view_name for word in search_words):
                    listbox_item.Visibility = Visibility.Visible
                else:
                    listbox_item.Visibility = Visibility.Collapsed

        if not search_text:
            for listbox_item in self.UI_listbox.Items:
                listbox_item.Visibility = Visibility.Visible



    def UIe_toggle_visibility(self,sender, e):
        # Sender = CheckBox because that's where event is coming from
        sheet = sender.Tag

        #⚠️ It's best to create a single transaction for all changes.
        # I'm too lazy to make it properly right now
        with Transaction(doc,'Change Sheet Visibiltiy Parameter') as t:
            t.Start()

            p_visibility = sheet.get_Parameter(BuiltInParameter.SHEET_SCHEDULED)
            value = 1 if p_visibility.AsInteger() ==0 else 0
            p_visibility.Set(value) #set opposite value from current one

            t.Commit()

    def UIe_btn_run(self, sender, e):
        print('Form Submitted!')
        self.Close()


# Show form to the user
UI = WPF_SheetToggle()

