# FL 2026 Audit — version/API/path dependencies

Scope: `rosasynthesiz/flstudio-mcp` v1.0.0 → **1.1.0 (FL 2026 port)**.
Evidence priority: local FL 2026 install (`FL64.exe` 26.1.7.5653,
`OneDrive\Belgeler\Image-Line\FL Studio\`) > official online manual
(`basics_new.htm`, `midi_scripting.htm`) > `IL-Group/FL-Studio-API-Stubs` >
factory scripts in `Settings\Hardware\` (Novation, MackieCU).

Status legend: `done` = ported+tested in CI, `manual` = needs live FL 2026.

| File:line | Dependency | Risk | Evidence | Action | Status |
|---|---|---|---|---|---|
| `fl_controller/.../device_FLStudioMCP.py:90` | `ui.getVersion()` only; no API version | med | Novation `fl.py:921` uses `general.getVersion()` as API version; MackieCU uses `ui.getVersion()` for display | Capture both in `OnInit`; expose via `ping`+`get_capabilities` | done |
| `device_FLStudioMCP.py:972` | `patterns.clonePattern(src)` single-arg | low | Manual: `clonePattern(index=-1, destIndex=-1) *43`; Novation `fl.py:768` two-arg | Try `clonePattern(src, dest)` when `dest>=0`, fall back to legacy | done |
| `device_FLStudioMCP.py` (new) | 2026-only entry points (`setPatternLength`, `clearPattern`, `showPicker`, `getSwing/setSwing`, `duplicatePatternData`, `movePattern`) | low | Manual `basics_new.htm` (2026, 26.1.1, 26.1.3) + manual patterns v39/v43/v44/v45 + `ui.showPicker` v41; Novation `fl.py:807`, `fl_constants.py:92` | `hasattr` probe in `get_capabilities`; no direct calls yet | done |
| `src/fl_studio_mcp/protocol.py` | Command catalogue has no capability command | low | — | Added `CMD_GET_CAPABILITIES` (additive; old peers ignore) | done |
| `src/fl_studio_mcp/capabilities.py` (new) | Version thresholds vs probe | low | Manual versions above; probe-first design | Single version-logic module; 2025 baseline fallback | done |
| `src/fl_studio_mcp/paths.py` (new) | `~/Documents` hardcodes break OneDrive/TR locale | **high** | Local user-data is `OneDrive\Belgeler\...`, not `Documents\...` | Robust roots + newest-first `FL Studio*`; env overrides | done |
| `music/plugin_library.py:find_plugin_db` | Assumes `.../Plugin database/Installed/` | **high** | Stock 2026 has `Effects/`, `Generators/`, `Installed.nfo` — **no `Installed/`** | Prefer `Installed/`; fall back to stock tree | done |
| `music/preset_library.py` | `~/Documents` + `Xfer` hardcodes | med | Same locale issue | `iter_fl_user_dirs()` + multi-root Xfer search | done |
| `pyscript_gen.py:19` | Hardcoded piano-roll scripts dir | med | `Settings\Piano roll scripts\` exists under OneDrive path | `resolve_scripts_dir()` at call time, legacy const as fallback | done |
| `tools/transport.py:fl_ping` | No version/capability info | low | — | Additive `capabilities` key, best-effort with fallback | done |
| `scripts/install_windows.bat:15` | `%USERPROFILE%\Documents\...` only | med | Same as paths | Scan Documents/OneDrive/Belgeler newest-first; `FL_SETTINGS` override | done |
| `scripts/install_macos.sh:7` | `$HOME/Documents/...` only | low | macOS unaffected by TR locale but multi-version possible | Newest-first scan; `FL_HARDWARE_OVERRIDE` | done |
| `connection.py` sysex path | 26.1.7 sysex freeze (bug 22604, UNVERIFIED no) | med | Repo never calls `GlobalTransport`; sysex already has 5 s timeout + heartbeat-stale errors | No new guard; clear `FLTimeout`/`FLNotRunning` messages kept | done |
| `mixer` menu / Audio Logger text | UI automation | none | Manual confirms rename; repo does no UI matching | Keep (verify in manual checklist) | manual |
| `FLEX` rebuild / Luxeverb +100 presets | Calibrated param curves drift | med | Manual confirms rebuild | Live `getParamName/Value` resolution kept; recalibration = manual test | manual |
| `Gopher` control / Audio Workgroups | Note-bridge `Cmd+Opt+Y` focus | low | Manual confirms both | Manual checklist item | manual |
| Metadata (`__version__` 0.3.0 vs 1.0.0; 14 vs 15 categories) | Version truth | low | `__init__.py:5`, `server.py:28-43` (15 packs), `README.md:68` | All bumped to 1.1.0; README category count left for upstream | done |
