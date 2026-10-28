// Run through Rhino MCP. Creates a NEW definition. Edit root for another computer.
using System;
using System.Linq;
var root="/Users/r2d2/Desktop/AI_arch_resources";
var canvas=Grasshopper.Instances.ActiveCanvas;
var doc=new Grasshopper.Kernel.GH_Document();
// Shared construction helpers for the teaching GH definitions.
var proxy=Grasshopper.Instances.ComponentServer.ObjectProxies.First(p=>p.Guid==new Guid("719467e6-7cf5-4848-99b0-c5dd57e5442c"));
Grasshopper.Kernel.GH_Component MakeScript(string name,string file,string[] inputs,string[] outputs,int x,int y){
 var comp=(Grasshopper.Kernel.GH_Component)Grasshopper.Instances.ComponentServer.EmitObjectProxy(proxy.Guid).CreateInstance();
 comp.CreateAttributes();comp.Name=name;comp.NickName=name;comp.Attributes.Pivot=new System.Drawing.PointF(x,y);
 var paramType=comp.Params.Input[0].GetType();
 foreach(var p in comp.Params.Input.ToArray())comp.Params.UnregisterInputParameter(p,true);
 foreach(var p in comp.Params.Output.Skip(1).ToArray())comp.Params.UnregisterOutputParameter(p,true);
 foreach(var n in inputs){var p=(Grasshopper.Kernel.IGH_Param)Activator.CreateInstance(paramType);p.Name=n;p.NickName=n;p.Description=n;p.Optional=false;p.Access=n=="footprints"?Grasshopper.Kernel.GH_ParamAccess.list:Grasshopper.Kernel.GH_ParamAccess.item;comp.Params.RegisterInputParam(p);}
 foreach(var n in outputs){var p=(Grasshopper.Kernel.IGH_Param)Activator.CreateInstance(paramType);p.Name=n;p.NickName=n;p.Description=n;p.Access=Grasshopper.Kernel.GH_ParamAccess.list;comp.Params.RegisterOutputParam(p);}
 comp.Params.OnParametersChanged();doc.AddObject(comp,false);
 var iface=comp.GetType().GetInterface("RhinoCodePlatform.GH.IScriptComponent");
 iface.GetProperty("MarshGuids").SetValue(comp,false);
 iface.GetProperty("Text").SetValue(comp,System.IO.File.ReadAllText(System.IO.Path.Combine(root,file)));
 comp.ExpireSolution(false);
 return comp;
}
Grasshopper.Kernel.Special.GH_NumberSlider Slider(string name,decimal min,decimal max,decimal value,int x,int y,int decimals){
 var s=new Grasshopper.Kernel.Special.GH_NumberSlider();s.CreateAttributes();s.NickName=name;
 s.Slider.Minimum=min;s.Slider.Maximum=max;s.Slider.DecimalPlaces=decimals;s.SetSliderValue(value);
 s.Attributes.Pivot=new System.Drawing.PointF(x,y);doc.AddObject(s,false);return s;
}
Grasshopper.Kernel.Special.GH_Panel Panel(string text,int x,int y,int width,int height){
 var p=new Grasshopper.Kernel.Special.GH_Panel();p.CreateAttributes();p.UserText=text;p.Attributes.Pivot=new System.Drawing.PointF(x,y);p.Attributes.Bounds=new System.Drawing.RectangleF(x,y,width,height);doc.AddObject(p,false);return p;
}
doc.FilePath=System.IO.Path.Combine(root,"20-toronto-envelope.gh");canvas.Document=doc;
Panel("PROMPT\nUse selected Toronto RD rules for a fictional lot.\nShow lot, geometric limits, and a two-storey house.\nCap the house by setbacks, height, coverage and FSI.\n\nASSUMED: RD(f15)(d0.6), 35% coverage, no HT value.\nCHANGE: lot depth 36 to 30 metres.",20,20,560,160);
var model=MakeScript("Toronto RD envelope","zoning_grasshopper.py",new[]{"lot_width","lot_depth"},new[]{"lot","envelope","house","report"},490,290);
var width=Slider("Lot width",15,21,15,40,240,1);
var depth=Slider("Lot depth",30,48,36,40,300,1);
model.Params.Input[0].AddSource(width);model.Params.Input[1].AddSource(depth);
var report=Panel("",720,20,560,660);report.AddSource(model.Params.Output[4]);

var io=new Grasshopper.Kernel.GH_DocumentIO();io.Document=doc;if(!io.SaveQuiet(doc.FilePath))throw new Exception("GH save failed");
canvas.Viewport.Zoom=1f;canvas.Viewport.Target=new System.Drawing.Point(0,0);canvas.Refresh();doc.NewSolution(false);
Console.WriteLine("Saved "+doc.FilePath);
