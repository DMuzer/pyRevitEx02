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
*** Сделать обход трубой
*** D:\18_проектирование\pyRevitExtension\DMuzer.extension\DMuzer FF.tab\Работа с коллизиями.panel\Сделать обход трубой.pushbutton\script.py
***************************************************************

***************************************************************
"""
print(st_str)
UI.TaskDialog.Show("DMuzer-скрипт", "Сделать обход трубой")


import System
import math

from Autodesk.Revit import *
from Autodesk.Revit.DB import *
from contextlib import contextmanager
import math, sys
import clr
import System
from System.Collections.Generic import IList, List
dut = 0.0032808398950131233
moveLength = 400 * dut

lib_path = r"D:\18_проектирование\98_PythonShell"
if not lib_path in sys.path :
	sys.path.append(lib_path)
	

check_print=True

pi2 = math.pi * 2

bic = BuiltInCategory
bip = DB.Structure.StructuralType
nonstr = bip.NonStructural
OT = UI.Selection.ObjectType

print("Обход трубой выше/ниже")

av = uidoc.ActiveView
vud = av.ViewDirection

def get_nearest_end_connector(element, pnt) :	
	if hasattr(element, "ConnectorManager") :
		return min([connector for connector\
							in element.ConnectorManager.Connectors
							if connector.ConnectorType == ConnectorType.End],
							key = lambda x : pnt.DistanceTo(x.Origin))
	else :
		return min([connector for connector 
							in element.MEPModel.ConnectorManager.Connectors
							if connector.ConnectorType == ConnectorType.End],
							key = lambda x : pnt.DistanceTo(x.Origin))

tr = False
if not doc.IsModifiable :
	tr = Transaction(doc, "1")
	tr.Start()
pl1 = Plane.CreateByNormalAndOrigin(av.ViewDirection, av.Origin)
sk_pl = SketchPlane.Create(doc, pl1)
av.SketchPlane = sk_pl
if tr :
	tr.Commit()

pipe_ref    = uidoc.Selection.PickObject(OT.Element)
pipe        = doc.GetElement(pipe_ref)

if not type(pipe) == Plumbing.Pipe :
	raise

p1_     = uidoc.Selection.PickPoint()
p2_     = uidoc.Selection.PickPoint()
p3_     = uidoc.Selection.PickPoint()

plc = pipe.Location.Curve
pdir = plc.Direction

t = clr.Reference[IList[ClosestPointsPairBetweenTwoCurves]](List[ClosestPointsPairBetweenTwoCurves]())
auxLine1 = Line.CreateUnbound(p1_, uidoc.ActiveView.ViewDirection)
plc.ComputeClosestPoints(auxLine1, True, False, False, t)

p1 = t.Item[0].XYZPointOnFirstCurve

t = clr.Reference[IList[ClosestPointsPairBetweenTwoCurves]](List[ClosestPointsPairBetweenTwoCurves]())
auxLine2 = Line.CreateUnbound(p2_, uidoc.ActiveView.ViewDirection)
plc.ComputeClosestPoints(auxLine2, True, False, False, t)

p2 = t.Item[0].XYZPointOnFirstCurve

t = clr.Reference[IList[ClosestPointsPairBetweenTwoCurves]](List[ClosestPointsPairBetweenTwoCurves]())
auxLine3 = Line.CreateUnbound(p3_, uidoc.ActiveView.ViewDirection)
plc.ComputeClosestPoints(auxLine3, True, False, False, t)

p3 = t.Item[0].XYZPointOnFirstCurve

v3 = p3_- p3

pDir = (p2 - p1).Normalize()

v3ud = vud.DotProduct(v3) * vud
v3pd = pdir.DotProduct(v3) * pdir

v3n = v3 - v3ud - v3pd



ptr_1 = p1 
if v3n.GetLength() >  pipe.Diameter * 5 :
	print("Опускаем вертикально")
	ptr_2 = p1 + v3n
	ptr_3 = p2 + v3n
	ptr_4 = p2
elif v3n.GetLength() >  pipe.Diameter * 2 :
	print("делаем переход под углом")
	ptr_2 = p1 + v3n + pDir * v3n.GetLength()
	ptr_4 = p2
	ptr_3 = p2 + v3n - pDir * v3n.GetLength()
else :
	print("делаем переход под углом")
	ptr_2 = p1 + v3n + pDir * v3n.GetLength() * 2
	ptr_4 = p2
	ptr_3 = p2 + v3n - pDir * v3n.GetLength() * 2
	
	

rl1 = Line.CreateBound(ptr_1, ptr_2)
rl2 = Line.CreateBound(ptr_2, ptr_3)
rl3 = Line.CreateBound(ptr_3, ptr_4)

print("---3")
points_ = [p1, p2, p3, ptr_1, ptr_2, ptr_3,ptr_4]
points =[]

for _p in points_ :
    _p1 = Point.Create(_p)
    points.append(_p1)

shapes = points + [
    rl1,
    rl2,
    rl3,
]

shapes_a = System.Array[GeometryObject](shapes)
tr = Transaction(doc, "add bypass")
tr.Start()
print("---4")
# ds = DirectShape.CreateElement(doc, ElementId(bic.OST_GenericModel))
# ds = ds.SetShape(shapes_a)

pipe2_id = Plumbing.PlumbingUtils.BreakCurve(doc, pipe.Id, p1)
pipe2 = doc.GetElement(pipe2_id)

if pipe.Location.Curve.Distance(p2) < pipe2.Location.Curve.Distance(p2) :
    pipe, pipe2 = pipe2, pipe

pipe3_id = Plumbing.PlumbingUtils.BreakCurve(doc, pipe2.Id, p2)
pipe3 = doc.GetElement(pipe3_id)

if pipe2.Location.Curve.Distance(p1) > pipe3.Location.Curve.Distance(p1) :
    pipe2, pipe3 = pipe3, pipe2

pipe_c1_id = ElementTransformUtils.CopyElement(doc, pipe2.Id, XYZ.Zero)[0]
pipe_c2_id = ElementTransformUtils.CopyElement(doc, pipe2.Id, XYZ.Zero)[0]
pipe_c3_id = ElementTransformUtils.CopyElement(doc, pipe2.Id, XYZ.Zero)[0]

pipe_c1 = doc.GetElement(pipe_c1_id)
pipe_c2 = doc.GetElement(pipe_c2_id)
pipe_c3 = doc.GetElement(pipe_c3_id)

pipe_c1.Location.Curve = rl1 
pipe_c2.Location.Curve = rl2
pipe_c3.Location.Curve = rl3

print("---5")

c_11, c_12 = get_nearest_end_connector(pipe, ptr_1), get_nearest_end_connector(pipe_c1, ptr_1)
c_21, c_22 = get_nearest_end_connector(pipe_c1, ptr_2), get_nearest_end_connector(pipe_c2, ptr_2)
c_31, c_32 = get_nearest_end_connector(pipe_c2, ptr_3), get_nearest_end_connector(pipe_c3, ptr_3)
c_41, c_42 = get_nearest_end_connector(pipe_c3, ptr_4), get_nearest_end_connector(pipe3, ptr_4)

doc.Create.NewElbowFitting(c_11, c_12)
doc.Create.NewElbowFitting(c_42, c_41)
doc.Create.NewElbowFitting(c_21, c_22)
elb3 = doc.Create.NewElbowFitting(c_32, c_31)
c_51 = get_nearest_end_connector(elb3, ptr_3)
doc.Delete(pipe2.Id)

tr.Commit()


















print(st_str)
print("ok...")