from Autodesk.Revit import DB, UI
from pyrevit import forms 
import time

uidoc = __revit__.ActiveUIDocument
uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)
count = 0
with forms.ProgressBar(title = "DMuzer progress", cancellable = True) as pb :
    while count < 100 :
        pb.update_progress(count, 100)
        count += 2
        time.sleep(0.2)
        if pb.cancelled : break
    