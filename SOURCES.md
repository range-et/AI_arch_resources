# Sources and model assumptions

Checked on 28 October 2026.

## Toronto example

The source is the City of Toronto's [RD zone regulations, section 10.20](https://www.toronto.ca/zoning/bylaw_amendments/ZBL_NewProvision_Chapter10_20.htm), with the [general residential rules, section 10.5](https://www.toronto.ca/zoning/bylaw_amendments/ZBL_NewProvision_Chapter10.htm).

| Input | Clause | Value used and condition |
| --- | --- | --- |
| Front yard | 10.20.40.70(1), 10.5.40.70(1) | 6 m; assume front-yard averaging does not apply. |
| Rear yard | 10.20.40.70(2) | Larger of 7.5 m and one-quarter lot depth. |
| Side yards | 10.20.40.70(3)(D) | 1.5 m each for an assumed required minimum frontage of 15 m. |
| Building length | 10.20.40.20(1) | 17 m for this assumed frontage; no extension used. |
| Overall height | 10.20.40.10(1)(B) | 10 m when no HT value applies. |
| Flat-roof main wall | 10.20.40.10(4)(A) | 7.5 m in this example. The selected box omits permitted upper-wall setbacks. |
| Coverage | 10.20.30.40(1)(A) | 35% is an assumed map value. |
| Floor space index | 10.20.40.40(1)(A) | 0.6 is an assumed zone-label value. The example is one detached dwelling without a secondary suite. |
| Minimum lot area | 10.20.30.10(1)(B) | 450 m² when the assumed f15 label has no a value. |

The lot is fictional. The assumed label is RD(f15)(d0.6), with no site exception, no HT or ST value, and no major-street condition. The two-storey house has equal floor plates and no floor-area exclusions. This example checks selected zoning dimensions. Ontario's Building Code, fire access, parking, landscaping, utilities and parcel-specific provisions are outside the model.

## Habitat 67

[Safdie Architects' project page](https://www.safdiearchitects.com/projects/habitat-67) is the reference for the built project. The generated model uses 126 assumed modules in three stepped groups. Its dimensions and placement are chosen for the classroom example. The JSON report records geometric validity separately from architectural fidelity.

## Autodesk

[Autodesk's Building Layout Explorer announcement](https://adsknews.autodesk.com/en/news/building-layout-explorer-in-autodesk-forma/) describes an experimental Forma Site Design feature for commercial users with US-stored data. It contains the vendor's multi-family and office demo videos. [The October 2026 Forma update](https://blogs.autodesk.com/forma/2026/10/14/what-autodesk-forma-announced-au-2026/) describes the continuing research.

The presentation uses an attributed excerpt of Autodesk's published multi-family demonstration. It does not represent a model generated in this local session. The LOD 200 claim has been removed because these sources do not establish it. The original vendor recording is available from the announcement page.

## LBM

[Jonathan Viquerat's source](https://github.com/jviquerat/lbm), commit `64023fc76db2ddb681b2d4d24306a433e85f9555`, supplies the numerical routines in `lbm_core.py`. The MIT licence is in `LBM_LICENSE.txt`. The local wrapper and GH adapter are documented in `README.md`.

## Rhino MCP

[McNeel's Codex setup instructions](https://mcneel.github.io/RhinoAI/docs/getting-started/codex/) document the Package Manager installation and Codex connection.
