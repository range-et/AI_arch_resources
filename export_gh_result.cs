// Export the active tower or zoning solution from its actual GH outputs.
using System;
using System.Linq;
var d=Grasshopper.Instances.ActiveCanvas.Document;
var c=d.Objects.OfType<Grasshopper.Kernel.GH_Component>().First(o=>o.Name=="Parametric tower"||o.Name=="Toronto RD envelope");
bool tower=c.Name=="Parametric tower";
var control=d.Objects.OfType<Grasshopper.Kernel.Special.GH_NumberSlider>().First(o=>o.NickName==(tower?"Total twist":"Lot depth"));
string suffix=control.CurrentValue==(tower?0:36)?"a":"b";
string stem=tower?"04-tower":"20-toronto-lot";
var root=System.IO.Path.GetDirectoryName(d.FilePath);
var file=new Rhino.FileIO.File3dm();file.Settings.ModelUnitSystem=Rhino.UnitSystem.Meters;
foreach(var o in __rhino_doc__.Objects.ToArray())__rhino_doc__.Objects.Delete(o,true);
var bounds=Rhino.Geometry.BoundingBox.Empty;
int n=0;
for(int i=1;i<c.Params.Output.Count-1;i++){
 var colour=tower?(i==1?System.Drawing.Color.BurlyWood:System.Drawing.Color.SteelBlue):(i==2?System.Drawing.Color.RoyalBlue:i==3?System.Drawing.Color.Coral:System.Drawing.Color.DimGray);
 var a=new Rhino.DocObjects.ObjectAttributes();a.Name=c.Params.Output[i].Name;a.ObjectColor=colour;a.ColorSource=Rhino.DocObjects.ObjectColorSource.ColorFromObject;
 if(!tower&&i==2)a.SetDisplayModeOverride(Rhino.Display.DisplayModeDescription.FindByName("Wireframe"));
 foreach(var goo in c.Params.Output[i].VolatileData.AllData(true)){
  var g=goo.ScriptVariable() as Rhino.Geometry.GeometryBase;if(g==null)continue;
  if(!g.IsValid)throw new Exception("Invalid output geometry");
  if(g is Rhino.Geometry.Brep b){if(!b.IsSolid)throw new Exception("Open output solid");file.Objects.AddBrep(b,a);}
  else if(g is Rhino.Geometry.Curve curve)file.Objects.AddCurve(curve,a);
  __rhino_doc__.Objects.Add(g,a);bounds.Union(g.GetBoundingBox(true));n++;
 }
}
file.Write(System.IO.Path.Combine(root,stem+"-"+suffix+".3dm"),8);
var report=c.Params.Output.Last().VolatileData.AllData(true).First().ToString();
System.IO.File.WriteAllText(System.IO.Path.Combine(root,stem+"-"+suffix+".json"),report);
__rhino_doc__.Views.Redraw();Console.WriteLine("Exported "+stem+" "+suffix+": "+n+" valid objects.\n"+report);
