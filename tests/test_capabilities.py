"""Capability layer tests (FL 2025 baseline vs FL 2026 paths)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fl_studio_mcp.capabilities import (
    baseline,
    describe,
    flags_from_api_version,
    merge_probe,
)


def test_baseline_all_off():
    caps = baseline("25.2.5")
    assert caps.has_set_pattern_length is False
    assert caps.has_clear_pattern is False
    assert caps.has_clone_dest is False
    assert caps.has_show_picker is False
    assert caps.source == "baseline"


def test_version_thresholds():
    v38 = flags_from_api_version(38)
    assert v38.has_set_pattern_length is False
    assert v38.has_clear_pattern is False

    v39 = flags_from_api_version(39)
    assert v39.has_set_pattern_length is True
    assert v39.has_increment_pattern_length is True
    assert v39.has_move_pattern is True
    assert v39.has_clear_pattern is False  # needs v44

    v43 = flags_from_api_version(43)
    assert v43.has_clone_dest is True
    assert v43.has_clear_pattern is False

    v44 = flags_from_api_version(44)
    assert v44.has_clear_pattern is True

    v45 = flags_from_api_version(45)
    assert v45.has_duplicate_pattern_data is True

    v41 = flags_from_api_version(41)
    assert v41.has_show_picker is True


def test_probe_overlays_version():
    base = flags_from_api_version(38)  # all False
    merged = merge_probe(
        base,
        {"set_pattern_length": True, "swing": True},
        fl_version="26.1.7",
    )
    assert merged.has_set_pattern_length is True
    assert merged.has_swing is True
    assert merged.has_clear_pattern is False
    assert merged.fl_version == "26.1.7"


def test_probe_never_clears_version_true():
    base = flags_from_api_version(44)  # clear True
    merged = merge_probe(base, {"clear_pattern": False})
    assert merged.has_clear_pattern is True


def test_probe_none_returns_base():
    base = flags_from_api_version(39)
    assert merge_probe(base, None) is base


def test_describe_json_safe():
    import json

    caps = flags_from_api_version(44, "26.1.3")
    json.dumps(describe(caps))
