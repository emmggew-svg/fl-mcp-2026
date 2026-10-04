"""Robust Image-Line user-data discovery (FL 2025 + 2026).

The old code hard-coded ``~/Documents/Image-Line/FL Studio`` which breaks
on OneDrive-redirected, localized (e.g. TR ``Belgeler``), or multi-version
machines. This module tries, in order:

1. Explicit env overrides (highest priority, documented per caller).
2. Known user-data roots: ``~/Documents/Image-Line``,
   ``~/OneDrive/Documents/Image-Line``, ``~/OneDrive/Belgeler/Image-Line``,
   ``~/Belgeler/Image-Line``.
3. Inside each root, ``FL Studio*`` folders sorted newest-first
   (so FL Studio 2026 wins over 2025 when both exist).

No new dependencies. Python 3.10 compatible.
"""

from __future__ import annotations

import os
from pathlib import Path


def _candidate_roots() -> list[Path]:
    home = Path.home()
    return [
        home / "Documents" / "Image-Line",
        home / "OneDrive" / "Documents" / "Image-Line",
        home / "OneDrive" / "Belgeler" / "Image-Line",
        home / "Belgeler" / "Image-Line",
        home / "Image-Line",
    ]


def iter_fl_user_dirs() -> list[Path]:
    """All ``FL Studio*`` user dirs, newest-first, deduplicated."""
    seen: list[Path] = []
    for root in _candidate_roots():
        if not root.is_dir():
            continue
        try:
            matches = sorted(root.glob("FL Studio*"), reverse=True)
        except OSError:
            continue
        for m in matches:
            if m.is_dir() and m not in seen:
                seen.append(m)
    # Explicit override dir (a full FL user dir) wins if given.
    override = os.environ.get("FLSTUDIO_MCP_USER_DIR")
    if override:
        p = Path(override)
        if p.is_dir() and p not in seen:
            seen.insert(0, p)
    return seen


def find_first_existing(*relative: str) -> str | None:
    """First ``<fl_user_dir>/<relative...>`` that exists (file or dir)."""
    for fl in iter_fl_user_dirs():
        p = fl.joinpath(*relative)
        if p.exists():
            return str(p)
    return None


def find_first_dir(*relative: str) -> str | None:
    """First ``<fl_user_dir>/<relative...>`` that is a directory."""
    for fl in iter_fl_user_dirs():
        p = fl.joinpath(*relative)
        if p.is_dir():
            return str(p)
    return None


def piano_roll_scripts_dir() -> str | None:
    """Where the daemon should write the generated ``MCP_Apply`` script."""
    env = os.environ.get("FLSTUDIO_MCP_PIANO_SCRIPTS")
    if env and Path(env).is_dir():
        return env
    return find_first_dir("Settings", "Piano roll scripts")


def plugin_db_installed_dir() -> str | None:
    """The ``.../Plugin database/Installed`` folder (third-party scans)."""
    env = os.environ.get("FLSTUDIO_MCP_PLUGIN_DB")
    if env and Path(env).is_dir():
        return env
    return find_first_dir("Presets", "Plugin database", "Installed")


def plugin_db_root() -> str | None:
    """Fallback: the stock ``.../Plugin database`` tree (no Installed/)."""
    for fl in iter_fl_user_dirs():
        p = fl / "Presets" / "Plugin database"
        if p.is_dir():
            return str(p)
    return None


def fl_presets_dir() -> str | None:
    """The ``.../Presets`` folder (stock + user presets)."""
    env = os.environ.get("FLSTUDIO_MCP_PRESETS")
    if env and Path(env).is_dir():
        return env
    return find_first_dir("Presets")
