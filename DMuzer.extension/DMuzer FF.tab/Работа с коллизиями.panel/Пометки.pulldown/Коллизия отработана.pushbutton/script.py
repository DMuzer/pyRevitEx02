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
*** Пометить отработанное пересечение
*** "D:\18_проектирование\98_PythonShell\СОЮЗ\Работа с пересечениями\04_Пометить отработанное пересечение.txt"
***************************************************************

***************************************************************
"""
print(st_str)
def setProcessed(collision) :
    collisionName = collision.LookupParameter("Наименование").AsString()
    print(collisionName)
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    tr = Transaction(doc, "Пометка отработанных коллизий")
    tr.Start()
    try :
        collision.LookupParameter("О_Примечание").Set("resolved")
        for view in views :
            if view.Name.Contains(collisionName+"_") :
                print("Найден вид")
                #print(f"{view.Name} - {type(view)}")
                param = view.LookupParameter("Вид_Подзаголовок")
                if param :
                    param.Set("resolved")
                else :
                    print("параметра нет...")
    except Exception as ex :
        TaskDialog.Show("asdf", str(ex))
        print(ex)
        
    tr.Commit() 
	
for collisionRef in uidoc.Selection.GetElementIds() :
    collision = doc.GetElement(collisionRef)
    if not isinstance(collision, DirectShape) : 
        continue
    try :
        setProcessed(collision)
    except :
        print("ошибка")
        pass
 
st_str = """
***************************************************************
*** Пометить отработанное пересечение
*** "D:\18_проектирование\98_PythonShell\СОЮЗ\Работа с пересечениями\04_Пометить отработанное пересечение.txt"
***************************************************************

***************************************************************
"""
print(st_str)
print("ok...")