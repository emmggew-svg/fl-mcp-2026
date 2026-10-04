"""FL version / API capability detection (FL 2025 + 2026).

Single place where version logic lives. Everything else imports flags
from here instead of sniffing versions inline.

Priority: capability probe (hasattr on the live FL modules, reported by
the controller) > API-version thresholds (official manual) > unknown
(assume 2025 baseline, all False).

Thresholds from the official MIDI scripting manual (midi_scripting.htm):
  v39: setPatternLength, incrementPatternLength, movePattern
  v41: ui.showPicker (plugin picker)
  v42: channels shuffle (swing lives in the same era; probed first)
  v43: clonePattern destIndex
  v44: clearPattern
  v45: duplicatePatternData
"""

from __future__ import annotations

from dataclasses import dataclass, field


# API version thresholds (see module docstring).
V_SET_PATTERN_LENGTH = 39
V_SHOW_PICKER = 41
V_CLONE_DEST = 43
V_CLEAR_PATTERN = 44
V_DUPLICATE_PATTERN_DATA = 45


@dataclass(frozen=True)
class FlCapabilities:
    """Feature flags for one connected FL Studio instance."""

    fl_version: str = "unknown"
    api_version: int | None = None
    has_set_pattern_length: bool = False
    has_increment_pattern_length: bool = False
    has_move_pattern: bool = False
    has_clear_pattern: bool = False
    has_clone_dest: bool = False
    has_show_picker: bool = False
    has_swing: bool = False
    has_duplicate_pattern_data: bool = False
    source: str = "unknown"
    notes: tuple[str, ...] = field(default_factory=tuple)


def _at_least(api_version: int | None, threshold: int) -> bool:
    return api_version is not None and api_version >= threshold


def flags_from_api_version(
    api_version: int | None, fl_version: str = "unknown"
) -> FlCapabilities:
    """Derive flags purely from the numeric API version (fallback path)."""
    return FlCapabilities(
        fl_version=fl_version,
        api_version=api_version,
        has_set_pattern_length=_at_least(api_version, V_SET_PATTERN_LENGTH),
        has_increment_pattern_length=_at_least(api_version, V_SET_PATTERN_LENGTH),
        has_move_pattern=_at_least(api_version, V_SET_PATTERN_LENGTH),
        has_clear_pattern=_at_least(api_version, V_CLEAR_PATTERN),
        has_clone_dest=_at_least(api_version, V_CLONE_DEST),
        has_show_picker=_at_least(api_version, V_SHOW_PICKER),
        has_swing=False,  # swing has no documented version; needs a probe
        has_duplicate_pattern_data=_at_least(
            api_version, V_DUPLICATE_PATTERN_DATA
        ),
        source="version",
    )


def merge_probe(
    base: FlCapabilities, probe: dict | None, fl_version: str | None = None
) -> FlCapabilities:
    """Overlay a live hasattr probe from the controller onto version flags.

    Probe keys (all optional bools): set_pattern_length,
    increment_pattern_length, move_pattern, clear_pattern, clone_dest,
    show_picker, swing, duplicate_pattern_data.
    """
    if not probe:
        return base
    get = probe.get
    # Start from base, flip to True wherever the probe confirms support.
    # A probe False never clears a version-derived True (probe may be stale).
    return FlCapabilities(
        fl_version=fl_version or base.fl_version,
        api_version=base.api_version,
        has_set_pattern_length=base.has_set_pattern_length
        or bool(get("set_pattern_length", False)),
        has_increment_pattern_length=base.has_increment_pattern_length
        or bool(get("increment_pattern_length", False)),
        has_move_pattern=base.has_move_pattern or bool(get("move_pattern", False)),
        has_clear_pattern=base.has_clear_pattern or bool(get("clear_pattern", False)),
        has_clone_dest=base.has_clone_dest or bool(get("clone_dest", False)),
        has_show_picker=base.has_show_picker or bool(get("show_picker", False)),
        has_swing=base.has_swing or bool(get("swing", False)),
        has_duplicate_pattern_data=base.has_duplicate_pattern_data
        or bool(get("duplicate_pattern_data", False)),
        source="probe+version" if base.source == "version" else "probe",
    )


def baseline(fl_version: str = "unknown") -> FlCapabilities:
    """2025 baseline: every 2026-only flag off. Safe fallback."""
    return FlCapabilities(fl_version=fl_version, source="baseline")


def describe(caps: FlCapabilities) -> dict:
    """JSON-safe snapshot for logs / fl_ping payloads."""
    return {
        "fl_version": caps.fl_version,
        "api_version": caps.api_version,
        "has_set_pattern_length": caps.has_set_pattern_length,
        "has_increment_pattern_length": caps.has_increment_pattern_length,
        "has_move_pattern": caps.has_move_pattern,
        "has_clear_pattern": caps.has_clear_pattern,
        "has_clone_dest": caps.has_clone_dest,
        "has_show_picker": caps.has_show_picker,
        "has_swing": caps.has_swing,
        "has_duplicate_pattern_data": caps.has_duplicate_pattern_data,
        "source": caps.source,
    }
