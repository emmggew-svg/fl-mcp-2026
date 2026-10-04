"""Tool-schema snapshot: the 67 public tool names are a frozen contract.

Static (AST-based, no fastmcp import needed): collects every
``def fl_*`` inside ``src/fl_studio_mcp/tools/*.py`` and compares
against the checked-in set. Any add/remove/rename fails loudly so
Phase 3's 'no schema change' promise is enforced by CI.
"""

import ast
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO / "src" / "fl_studio_mcp" / "tools"

EXPECTED = frozenset(
    """
fl_ping fl_get_tempo fl_set_tempo fl_play fl_stop fl_toggle_play fl_record
fl_get_play_state fl_get_song_position fl_set_song_position
fl_get_project_state fl_get_mixer_state fl_get_channel_state
fl_set_mixer_volume fl_set_mixer_pan fl_set_mixer_mute fl_set_mixer_solo
fl_set_mixer_name fl_set_channel_volume fl_set_channel_pan fl_set_channel_mute
fl_set_channel_solo fl_take_snapshot fl_rollback_last_change fl_set_dry_run
fl_arrange_new_pattern fl_arrange_select_channel fl_arrange_clone_pattern
fl_arrange_add_marker
fl_diagnose_mix fl_apply_mix_fix fl_mix_watch_start fl_mix_watch_status
fl_mix_watch_stop fl_gain_stage fl_reference_match
fl_apply_eq_intent fl_apply_reverb_intent fl_apply_delay_intent
fl_get_track_level fl_apply_compression_intent
fl_get_routing fl_get_routing_all fl_get_channel_routing
fl_detect_cleanup_candidates fl_set_route fl_group_tracks
fl_plugin_list fl_plugin_get_params fl_plugin_set_param
fl_write_piano_roll_notes fl_quantize_pattern
fl_write_raga_melody fl_write_raga_chords
fl_list_chains fl_list_installed_plugins fl_setup_chain
fl_list_presets fl_suggest_preset
fl_solo_tracks fl_mute_tracks fl_clear_mute_solo
fl_set_track_color fl_set_channel_color
fl_analyze_audio fl_extract_melody
fl_export_midi
""".split()
)


def collect_tool_names():
    found = set()
    for py in sorted(TOOLS_DIR.glob("*.py")):
        if py.name == "__init__.py":
            continue
        tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("fl_"):
                    found.add(node.name)
    return found


def test_tool_count_is_67():
    assert len(collect_tool_names()) == 67


def test_tool_names_match_snapshot():
    found = collect_tool_names()
    assert found == set(EXPECTED), (
        "tool set changed!\nadded=%s\nremoved=%s"
        % (sorted(found - set(EXPECTED)), sorted(set(EXPECTED) - found))
    )


def test_ping_reports_capabilities_best_effort():
    # fl_ping must include the additive capabilities report (FL 2026 port)
    # without renaming any tool.
    src = (TOOLS_DIR / "transport.py").read_text(encoding="utf-8")
    assert '"capabilities"' in src
    assert "CMD_GET_CAPABILITIES" in src


def test_controller_probe_handler_registered():
    ctrl = (
        REPO / "fl_controller" / "FLStudioMCP" / "device_FLStudioMCP.py"
    ).read_text(encoding="utf-8")
    assert '"get_capabilities": _h_get_capabilities' in ctrl
    assert "clonePattern(src, dest)" in ctrl
