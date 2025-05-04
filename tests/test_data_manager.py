# tests/test_data_manager.py
"""
Unit‑tests for data/data_manager.py
"""

import builtins
import json
import logging
import pytest

from data.data_manager import (
    load_animals,
    save_animals,
    replace_all_animals,
)


def test_load_returns_list(tmp_json):
    animals = load_animals(tmp_json)
    assert isinstance(animals, list)
    assert len(animals) == 4


def test_load_missing_file_returns_empty(tmp_path):
    missing = tmp_path / "nowhere.json"
    assert load_animals(missing) == []


def test_save_appends(tmp_path):
    file_ = tmp_path / "dogs.json"

    save_animals(file_, [{"name": "Fido"}])
    save_animals(file_, [{"name": "Molly"}])

    names = {a["name"] for a in load_animals(file_)}
    assert names == {"Fido", "Molly"}


def test_replace_overwrites(tmp_json):
    new = [{"name": "OnlyOne"}]
    replace_all_animals(tmp_json, new)
    assert json.loads(tmp_json.read_text()) == new


def test_load_returns_empty_on_bad_json(tmp_path, caplog):
    bad = tmp_path / "corrupt.json"
    bad.write_text("{not: valid json]", encoding="utf-8")

    caplog.clear()
    assert load_animals(bad) == []
    assert "invalid json" in caplog.text.lower()


def test_load_animals_when_json_is_not_list(tmp_path, caplog):
    bad = tmp_path / "not_list.json"
    bad.write_text('{"name": "Oops"}')

    caplog.clear()
    assert load_animals(bad) == []
    assert "not a list" in caplog.text.lower()


def test_save_rejects_non_list(tmp_path, caplog):
    file_ = tmp_path / "out.json"

    caplog.clear()
    save_animals(file_, {"name": "Fido"})         # wrong top‑level type

    assert "must be a list" in caplog.text.lower()
    assert not file_.exists()


def test_replace_all_rejects_bad_data(tmp_path, caplog):
    file_ = tmp_path / "out.json"

    caplog.clear()
    replace_all_animals(file_, {"not": "a list"})

    assert "must be a list" in caplog.text.lower()
    assert not file_.exists()


def test_load_handles_io_error(monkeypatch):
    def _raise(*args, **kwargs):
        raise OSError("boom")

    monkeypatch.setattr(builtins, "open", _raise)

    with pytest.raises(OSError):
        load_animals("dummy.json")


def test_save_animals_overwrites_nonlist_file(tmp_path, caplog):
    """
    Existing file contains JSON that loads, but isn't a list.
    save_animals() should warn and start with an empty list.
    """
    file_ = tmp_path / "mixed.json"
    file_.write_text('{"wrong": "shape"}')

    caplog.set_level(logging.WARNING)
    save_animals(file_, [{"name": "Fido"}])

    assert "not a list" in caplog.text.lower()
    assert load_animals(file_) == [{"name": "Fido"}]


def test_save_animals_overwrites_invalid_json(tmp_path, caplog):
    """
    Existing file contains broken JSON → JSONDecodeError branch.
    """
    file_ = tmp_path / "badjson.json"
    file_.write_text("{ bad json ]")

    caplog.set_level(logging.WARNING)
    save_animals(file_, [{"name": "Buddy"}])

    assert "invalid json" in caplog.text.lower()
    assert load_animals(file_) == [{"name": "Buddy"}]


def test_save_animals_handles_unexpected_exception(tmp_path, monkeypatch, caplog):
    file_ = tmp_path / "io_fail.json"
    monkeypatch.setattr(json, "dump", lambda *a, **k: (_ for _ in ()).throw(TypeError("boom")))
    caplog.set_level(logging.ERROR)

    save_animals(file_, [{"name": "Rex"}])
    assert "error saving to" in caplog.text.lower()


def test_replace_all_animals_handles_unexpected_exception(tmp_path, monkeypatch, caplog):
    file_ = tmp_path / "io_fail.json"
    monkeypatch.setattr(json, "dump", lambda *a, **k: (_ for _ in ()).throw(TypeError("boom")))
    caplog.set_level(logging.ERROR)

    replace_all_animals(file_, [{"name": "Rex"}])
    assert "error saving data to" in caplog.text.lower()
