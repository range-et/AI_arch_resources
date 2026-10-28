"""Run through Rhino MCP's run_python tool after installation."""
import Rhino
import System

doc = __rhino_doc__
layer = Rhino.DocObjects.Layer()
layer.Name = 'MCP install check'
layer_index = doc.Layers.FindByFullPath(layer.Name, -1)
if layer_index < 0:
    layer_index = doc.Layers.Add(layer)
attributes = Rhino.DocObjects.ObjectAttributes()
attributes.Name = 'MCP torus: major radius 10, minor radius 2'
attributes.LayerIndex = layer_index
geometry = Rhino.Geometry.Torus(Rhino.Geometry.Plane.WorldXY, 10.0, 2.0).ToBrep()
assert geometry.IsValid and geometry.IsSolid
object_id = doc.Objects.AddBrep(geometry, attributes)
assert object_id != System.Guid.Empty
Rhino.RhinoApp.WriteLine('MCP check passed: one valid closed torus. Major radius 10, minor radius 2.')
doc.Views.Redraw()
print(str(object_id))
