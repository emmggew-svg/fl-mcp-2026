# FL 2026 Manual Test Checklist (FL Studio 26.1.7, Windows)

Live-DAW checks the sandbox cannot run. Work through top to bottom inside
real FL Studio 2026. Mark pass/fail. Anything failing → file an issue with
the `fl_ping` output attached.

| # | Check | Expected | Pass |
|---|---|---|---|
| 1 | Ports `FLStudioMCP RX` + `FLStudioMCP TX` created (loopMIDI) | Both listed | ☐ |
| 2 | `scripts\install_windows.bat` on OneDrive/TR machine | Finds `OneDrive\Belgeler\Image-Line\FL Studio\Settings` | ☐ |
| 3 | MIDI Settings: RX input (type FLStudioMCP, port 42) + TX output (port 42) | `[FLStudioMCP] Ready. FL 26.x, protocol v2.` in Script output | ☐ |
| 4 | `fl-studio-mcp-daemon` running | Holds ports, no crash | ☐ |
| 5 | `fl_ping` | `alive:true`, `fl_version` 26.x, `api_version` ≥ 39, `capabilities.has_clone_dest:true`, `has_clear_pattern:true` (≥26.1.3) | ☐ |
| 6 | Transport: play/stop/tempo get+set | Round-trips, readback matches | ☐ |
| 7 | Mixer + channel read/write + `fl_take_snapshot` → `fl_rollback_last_change` | Write → readback → rollback restores | ☐ |
| 8 | `fl_arrange_new_pattern` → `fl_write_piano_roll_notes` (armed `MCP_Apply`) | Notes land in the new pattern | ☐ |
| 9 | `fl_arrange_clone_pattern` (no dest) | Clone + rename, count +1 | ☐ |
| 10 | `fl_arrange_add_marker` | Marker at bar, undo removes it | ☐ |
| 11 | `fl_plugin_get_params` / `fl_plugin_set_param` on stock + 3rd-party plugin | Live names resolve; set → readback | ☐ |
| 12 | `fl_list_installed_plugins` on stock 2026 (no `Installed/`) | Falls back to stock tree, non-empty | ☐ |
| 13 | `fl_export_midi` → File > Import MIDI | File under `~/.flstudio-mcp/exports/`, imports cleanly | ☐ |
| 14 | Mix Doctor full pass + one gated fix | Evidence cited, snapshot → write → readback → rollback works | ☐ |
| 15 | Piano-roll `MCP_Apply` re-arm after FL restart | One run from scripting menu re-arms | ☐ |
| 16 | Soak: 15 min idle + rapid tool calls | No sysex freeze, no `FLTimeout` storm | ☐ |
| 17 | (macOS only) `Cmd+Opt+Y` trigger + Accessibility grant | Notes written without manual focus | ☐ |
