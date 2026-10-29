# AI in Architecture

The root contains the presentation and this guide. Each numbered demo folder holds its video, code, models and reports. Play the MP4s inside the [Google Slides deck](https://docs.google.com/presentation/d/1VEH2NRa5f1dJzQgTBd2cGdW-wjFdS8-PpCOyl6bzqpc/edit).

## Videos for the talk

| Slide | Video | Length | What it shows |
| --- | --- | --- | --- |
| 16 | [Rhino MCP installation](demo-1-install/01-rhino-mcp-install.mp4) | 1:54 | Package download and installation, Rhino restart, Codex connection, listener start and a torus made through MCP. |
| 18 | [Rhino command selection](demo-2-commands/02-command-selection.mp4) | 0:40 | Radial profile, Revolve, Cap and a valid closed dome. |
| 20 | [Build Habitat 67](demo-3-habitat/03-habitat-prompt.mp4) | 0:29 | Run a coordinate script and inspect its approximate massing. |
| 22 | [Parametric tower](demo-4-tower/04-parametric-tower.mp4) | 1:06 | Create a GH definition, run its Python component and change twist from 0 to 60 degrees. |
| 24 | [LBM to Grasshopper](demo-5-lbm/05-lbm-to-grasshopper.mp4) | 1:52 | Read the source, inspect the port, build and run the GH tool, move a footprint and compare solved fields. |
| 26 | [Toronto zoning example](demo-6-zoning/20-toronto-zoning.mp4) | 1:07 | Read official clauses, run the GH component and change lot depth. |
| 28 | [Autodesk published demo](demo-7-autodesk/21-autodesk-published-demo.mp4) | 0:23 | An attributed excerpt of Autodesk's experimental Building Layout Explorer. |

All videos were captured with **OBS Studio**. They are silent, with captions. The edited videos combine process footage and result shots. Faster sections are labelled. The local demos use working Rhino and Grasshopper scripts. The Autodesk clip is the vendor's published example; it was not generated in a local Forma account.

Each explanation now has a following slide with the actual Drive MP4 inserted as a playable video. Click the video in slideshow mode. The files are in the UofT Drive folder. Use the online Google Slides deck for playback. The PowerPoint export retains poster images and Drive links. Keep the local MP4s as a backup. The Autodesk explanation retains the original keynote link as an additional reference.

## Open the tools

Use Rhino 8 with Grasshopper and the Python 3 component. These demos ran in Rhino 8.36 on Apple Silicon. Keep each demo folder intact when copying the tools.

| Tool | Open in Grasshopper | Change | Expected result |
| --- | --- | --- | --- |
| Tower | `04-parametric-tower.gh` | **Total twist**: 0 to 60 | 12 closed slab solids and one closed core, with changed rotations. |
| Flow slice | `05-lbm-tool.gh` | **Middle block shift**: 0 to -12 | A different obstacle mask and flow field. Both reports show finite values and positive density. |
| Toronto lot | `20-toronto-envelope.gh` | **Lot depth**: 36 to 30 | Rear setback changes from 9 m to 7.5 m. Example floor area changes from 324 m² to 270 m². |

The GH files contain their component scripts. The flow component loads `lbm_solver.py` and `lbm_core.py` from its demo folder. Its `# r: numpy` directive loads NumPy through Rhino's Python environment. The zoning component loads `zoning_rules.py` and `toronto-lot.json`. Wait for the initial solution before changing a slider.

`build_parametric_gh.cs`, `build_lbm_gh.cs` and `build_zoning_gh.cs` rebuild the definitions through Rhino MCP's `run_csharp` tool. Each creates a new GH document. Change the `root` path in these builders if you move the folder. The standalone Rhino scripts also have a `root` path to update when relocating them.

`tools/export_gh_result.cs` exports the active tower or zoning solution to Rhino and saves its model and report. `export_lbm.cs` does the same for the flow slice. Exports help when GH preview disappears after hiding its window. The recordings show the component inputs and reports, then the exported geometry.

## Rhino MCP installation

In Rhino, run `PackageManager` and install **Rhino-MCP-Platform**. Restart Rhino. Run `MCPConnect` and click **Install** next to Codex. Restart Codex to load its tools, then run `MCPStart` in Rhino.

The video records the actual package download and installation, Rhino restart, connection setup and the model check. Codex was already running during the recording; its restart is described in the instructions. See [McNeel's setup guide](https://mcneel.github.io/RhinoAI/docs/getting-started/codex/).

`install_check.py` creates one torus through MCP and checks its validity and closure. Its saved result is `01-install-check.3dm`.

## Command and mesh examples

`02_command_selection.py` creates a radial profile. In Rhino, revolve it through a full circle about **World Z**, then cap it. `02_check_dome.py` checks the result. `02-command-selection.3dm` contains the hidden profile and one valid closed dome. The report is `02-command-checks.json`.

`03_habitat_prompt.py` interprets **Build Habitat 67** as an approximate massing study. It builds raw mesh coordinates for 126 assumed modules. The saved mesh is valid and closed, with 1,008 vertices and 756 quad faces. Dimensions and layout are assumptions. It does not reconstruct the original plans, structure or circulation. Compare it with [Safdie Architects' project](https://www.safdiearchitects.com/projects/habitat-67). Files: `03-habitat-massing.3dm` and `03-habitat-checks.json`.

## LBM adaptation

The source is [Jonathan Viquerat's LBM project](https://github.com/jviquerat/lbm), commit `64023fc76db2ddb681b2d4d24306a433e85f9555`. Its MIT licence is in `LBM_LICENSE.txt`.

`lbm_core.py` retains the upstream numerical routines, removes Numba imports and decorators, and replaces `nb.prange` with `range`. `lbm_solver.py` provides the grid, obstacle links, initial conditions, time loop and checks. `lbm_grasshopper.py` converts closed World XY footprints into an obstacle mask, then returns a coloured mesh, velocity segments and a report. `lbm_footprints.py` supplies the example geometry. The full adaptation prompt is in `lbm_prompt.txt`.

Both layouts use D2Q9/TRT, a 160 × 64 grid, 1,800 steps, inlet peak 0.03 and tau 0.65. Boundary conditions are a parabolic inlet, pressure outlet, no-slip channel walls and halfway bounce-back at obstacles. One coordinate unit is one lattice cell.

| Check | Layout A, shift 0 | Layout B, shift -12 |
| --- | ---: | ---: |
| Peak speed, lattice units | 0.0559223 | 0.0498592 |
| Footprint cells | 480 | 480 |
| Mesh faces | 10,240 | 10,240 |
| Velocity segments | 152 | 152 |
| Finite values and positive density | Passed | Passed |

The same colour scale applies to both fields. Blue is slow and yellow is fast relative to the inlet peak. The segments indicate local velocity. `05-lbm-layout-a.3dm` and `05-lbm-layout-b.3dm` contain actual GH outputs, with corresponding JSON reports.

This is a 2D laminar channel teaching model in lattice units. Physical accuracy and grid convergence have not been assessed. Vertical flow and atmospheric boundary conditions are omitted.

## Toronto example

The fictional lot assumes **RD(f15)(d0.6)**, a detached house without a secondary suite, no site exceptions, and no HT or ST value. It uses selected [Toronto RD zoning clauses](https://www.toronto.ca/zoning/bylaw_amendments/ZBL_NewProvision_Chapter10_20.htm). Front-yard averaging is assumed inapplicable. Coverage of 35% is an assumed map value. [SOURCES.md](SOURCES.md) gives the clauses and conditions.

The GH tool uses a simplified box for selected geometric limits and a two-storey example house. `20-toronto-lot-a.3dm` and `20-toronto-lot-b.3dm` contain both lot cases and have matching JSON reports. No real parcel, complete zoning review or Ontario Building Code compliance has been checked.

## Checks and file rules

With Python, NumPy and rhino3dm installed:

```sh
python demo-5-lbm/check_lbm.py
python tools/verify_demos.py
```

`05-lbm-checks.json` records a standalone reproduction of both GH flow results. `tools/demo-checks.json` records model readback, zoning calculations, slide labels and video formats. All three GH files were reopened and solved without component errors before delivery.

The root holds the deck, README, sources and demo plan. Numbered demo folders hold their final artifacts. Shared recording, export and check scripts are in `tools/`. **`working/` is gitignored**. It holds notes, old attempts, raw OBS recordings, local dependencies and temporary cuts. `tools/recordings.json` lists the source times and edits. `tools/edit_recordings.py` recreates the final cuts from the raw MOV files using ffmpeg and Pillow.

## Folder map

| Folder | Contents |
| --- | --- |
| `demo-1-install/` | Rhino MCP installation and torus check |
| `demo-2-commands/` | Native command sequence and dome |
| `demo-3-habitat/` | Approximate Habitat massing |
| `demo-4-tower/` | Parametric tower |
| `demo-5-lbm/` | Source port, flow tool and two layouts |
| `demo-6-zoning/` | Toronto rules, translucent envelope and annotated models |
| `demo-7-autodesk/` | Attributed vendor excerpt |
| `tools/` | Shared scripts, video edit manifest and checks |
| `working/` | Ignored scratch files, old attempts and raw recordings |

The zoning tool uses an 82% transparent blue preview. The baked model uses a dedicated display mode with transparency on both front and back faces. `demo-6-zoning/annotate_zoning.py` adds the setback and height labels and saves `20-toronto-annotated-a.3dm` and `20-toronto-annotated-b.3dm`. The example house sits 0.1 m inside the envelope at the front and sides so the surfaces remain distinct. Its floor area still follows the same FSI cap.
