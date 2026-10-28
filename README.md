# AI in Architecture

Open the presentation, then play the two OBS recordings:

- [Rhino MCP installation](01-rhino-mcp-install.mp4) — 1 min 54 sec. Package Manager download and install, Rhino restart, Codex connection, listener start, and a torus made through MCP.
- [LBM to Grasshopper](05-lbm-to-grasshopper.mp4) — 3 min 42 sec. Read the GitHub source, build the definition, inspect and repair a curve input error, run the solver, move a building, and inspect the changed field. The first two sections play at 2× speed; cuts are labelled.
- [Full Grasshopper session](05-lbm-full-session.mp4) — the continuous OBS capture, including pauses and setup repairs. The source review is included in the short walkthrough.

These are recordings of the software running. They have no narration. The short LBM video has captions.

## Open the Grasshopper tool

1. Use Rhino 8 with Grasshopper and Python 3.
2. Keep `05-lbm-tool.gh`, `lbm_solver.py` and `lbm_core.py` together in this folder.
3. Open `05-lbm-tool.gh`. Allow the Python component to load NumPy through its `# r: numpy` directive.
4. Wait for the solution. The report panel should show `finite: true`, `positive_density: true`, three footprints and 10,240 mesh faces.
5. Set **Middle block shift** from **0** to **-12**. Grasshopper recomputes the field.

The definition contains the footprint and adapter scripts. Their editable copies are `lbm_footprints.py` and `lbm_grasshopper.py`. Inputs are closed curves on World XY. One coordinate unit is one lattice cell. Colours use the same scale for both layouts: blue is slow and yellow is fast, relative to the inlet peak. Line segments show local velocity direction.

The `.3dm` files `05-lbm-layout-a.3dm` and `05-lbm-layout-b.3dm` contain exports of the actual Grasshopper outputs. `export_lbm.cs` exports the current solution and updates a Rhino layer named **LBM current result**. This is also useful if the live GH preview disappears when its window is hidden. The video shows this export step.

## What changed in the code

The source is [Jonathan Viquerat's LBM project](https://github.com/jviquerat/lbm), commit `64023fc76db2ddb681b2d4d24306a433e85f9555`. Its MIT licence is in `LBM_LICENSE.txt`.

`lbm_core.py` retains the source file's numerical routines, removes Numba decorators, and replaces `nb.prange` with `range`. `lbm_solver.py` supplies the grid, obstacle links, starting values, time loop and checks. The GH adapter turns closed footprints into an obstacle mask and turns the result into a coloured mesh and velocity segments. `lbm_prompt.txt` holds the adaptation prompt. `build_lbm_gh.cs` rebuilds the definition through Rhino MCP; edit its `root` path before using it on another computer.

Both runs use D2Q9 with TRT collision, a 160 × 64 grid and 1,800 time steps. The inlet peak is 0.03; tau is 0.65. The channel has a parabolic inlet, pressure outlet, no-slip top and bottom walls, and halfway bounce-back at obstacles.

| Check | Layout A: shift 0 | Layout B: shift -12 |
| --- | ---: | ---: |
| Peak speed, lattice units | 0.0559223 | 0.0498592 |
| Footprint cells | 480 | 480 |
| Mesh faces | 10,240 | 10,240 |
| Finite values and positive density | Passed | Passed |

`05-lbm-layout-a.json` and `05-lbm-layout-b.json` are reports read from the GH outputs. `check_lbm.py` reruns both layouts outside Rhino and compares peak speeds with those reports. It also checks that the fields differ. Results are in `05-lbm-checks.json`.

Run the check with Python and NumPy installed:

```sh
python check_lbm.py
```

This is a 2D laminar channel example in lattice units. Physical accuracy and grid convergence have not been assessed. It omits vertical flow and atmospheric boundary conditions.

## Installation check

The install recording uses Rhino 8.36 and Rhino-MCP-Platform 0.3.0 on Apple Silicon. The sequence is `PackageManager` → install **Rhino-MCP-Platform** → restart Rhino → `MCPConnect` → **Codex Install** → restart Codex to reload its tools → `MCPStart` in Rhino. The recording captures the package installation, Rhino restart and connection check. Codex was already running in the recording session.

`install_check.py` creates one torus through Rhino MCP and checks that it is a valid closed solid. The saved object is in `01-install-check.3dm`.

[McNeel's setup guide](https://mcneel.github.io/RhinoAI/docs/getting-started/codex/) describes the connection steps.

## Presentation and remaining demos

`AI in Architecture - Presentation.pptx` is exported from the existing Google Slides deck. Slides 15 and 19 now match the install commands and the TRT port. Source details and model limits are in the speaker notes. See `DEMO_PLAN.md` for the slide inventory and the remaining recordings.

The Toronto files are a separate teaching example: `toronto-lot.json`, `build_zoning.py`, `20-toronto-lot.3dm` and `20-zoning-calculation.json`. They use a fictional 15 × 36 m lot and selected [Toronto RD zoning rules](https://www.toronto.ca/zoning/bylaw_amendments/ZBL_NewProvision_Chapter10_20.htm). Coverage and FSI are declared assumptions. No real parcel or full code compliance has been checked. Its recording is still pending.

## Folder rules

All deliverable code, models, reports, recordings and the deck are directly in this folder. `working/` is gitignored and holds old attempts, notes, downloaded source, the local Python environment, raw OBS files and temporary video cuts. Earlier standalone flow animations are archived there.
