"""Path discovery tests (OneDrive + localized Documents safe)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fl_studio_mcp import paths


def test_candidate_roots_include_onedrive_and_tr_locale():
    roots = [str(p) for p in paths._candidate_roots()]
    assert any("OneDrive" in r for r in roots)
    assert any("Belgeler" in r for r in roots)


def test_env_override_wins(tmp_path, monkeypatch):
    fake = tmp_path / "FL Studio 2026"
    (fake / "Presets" / "Plugin database" / "Installed").mkdir(parents=True)
    installed = fake / "Presets" / "Plugin database" / "Installed"
    monkeypatch.setenv("FLSTUDIO_MCP_PLUGIN_DB", str(installed))
    assert paths.plugin_db_installed_dir() == str(installed)


def test_iter_fl_user_dirs_returns_list():
    # Must not raise on machines without FL installed; env override may add one.
    assert isinstance(paths.iter_fl_user_dirs(), list)
