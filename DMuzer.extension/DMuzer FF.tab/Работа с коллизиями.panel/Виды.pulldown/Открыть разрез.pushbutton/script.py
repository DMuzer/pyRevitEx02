# -*- coding: utf-8 -*-
from Autodesk.Revit import DB, UI
from Autodesk.Revit.DB import *
from pyrevit import forms 
import time

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
#uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)


st_str = """
***************************************************************
*** Открыть  разре вид коллизии
*** D:\18_проектирование\pyRevitExtension\DMuzer.extension\DMuzer FF.tab\Работа с коллизиями.panel\Открыть 3D.pushbutton\script.py
***************************************************************

***************************************************************
"""
print(st_str)
#UI.TaskDialog.Show("DMuzer-скрипт", "Открыть 3Д вид коллизии")
def setProcessed(collision) :
    collisionName = collision.LookupParameter("Наименование").AsString()
    print(collisionName)
    views = FilteredElementCollector(doc).OfClass(ViewSection).ToElements()
    #tr = Transaction(doc, "Пометка отработанных коллизий")
    #tr.Start()
    try :
        #collision.LookupParameter("О_Примечание").Set("Отработано")
        for view in views :
            if view.Name.Contains(collisionName+"_") :
                print("Найден вид")
                uidoc.ActiveView = view 

    except Exception as ex :
        UI.TaskDialog.Show("asdf", str(ex))
        print(ex)
        
    #tr.Commit() 
	
for collisionRef in uidoc.Selection.GetElementIds() :
    collision = doc.GetElement(collisionRef)
    if not isinstance(collision, DirectShape) : 
        continue
    try :
        setProcessed(collision)
    except :
        print("ошибка")
        pass
 

print(st_str)
print("ok...")