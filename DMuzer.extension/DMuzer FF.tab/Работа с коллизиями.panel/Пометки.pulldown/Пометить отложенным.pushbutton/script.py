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
*** Пометить отложенным
*** D:\\18_проектирование\pyRevitExtension\\DMuzer.extension\\DMuzer FF.tab\\Работа с коллизиями.panel\Пометить отложенным.pushbutton\script.py
***************************************************************

***************************************************************
"""
#print(st_str)
#UI.TaskDialog.Show("Сообщение", "Функция пометить отложенным")
def setProcessed(collision) :
    collisionName = collision.LookupParameter("Наименование").AsString()
    print(collisionName)
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    tr = Transaction(doc, "Пометка отработанных коллизий")
    tr.Start()
    try :
        collision.LookupParameter("О_Примечание").Set("suspended")
        for view in views :
            if view.Name.Contains(collisionName+"_") :
                #print("Найден вид")
                #print(f"{view.Name} - {type(view)}")
                param = view.LookupParameter("Вид_Подзаголовок")
                if param :
                    param.Set("suspended")
                else :
                    print("параметра нет...")
    except Exception as ex :
        
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
 
#print(st_str)
#print("ok...")