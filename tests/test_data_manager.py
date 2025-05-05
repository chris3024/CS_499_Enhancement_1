import json
import logging
from data.data_manager import load_animals, save_animals, replace_all_animals


def test_load_returns_list(tmp_json):
    animals = load_animals(tmp_json)
    assert isinstance(animals, list)
    assert len(animals) == 4


def test_load_handles_missing_and_bad_json(tmp_path, caplog):
    missing = tmp_path / "missing.json"
    corrupt = tmp_path / "bad.json"
    not_list = tmp_path / "notlist.json"

    corrupt.write_text("{ bad json ]")
    not_list.write_text('{"key": "value"}')

    caplog.clear()
    assert load_animals(missing) == []
    assert load_animals(corrupt) == []
    assert load_animals(not_list) == []

    assert any("file not found" in msg.message.lower() or "json decode error" in msg.message.lower()
               for msg in caplog.records)


def test_save_appends_to_file(tmp_path):
    file_ = tmp_path / "dogs.json"
    save_animals(file_, [{"name": "Fido"}])
    save_animals(file_, [{"name": "Molly"}])
    names = {a["name"] for a in load_animals(file_)}
    assert names == {"Fido", "Molly"}


def test_save_animals_recovers_from_invalid_or_nonlist_files(tmp_path, caplog):
    not_list = tmp_path / "notlist.json"
    bad_json = tmp_path / "bad.json"

    not_list.write_text('{"oops": 1}')
    bad_json.write_text("{ bad json ]")

    caplog.clear()
    save_animals(not_list, [{"name": "Fido"}])
    save_animals(bad_json, [{"name": "Rex"}])

    assert load_animals(not_list) == [{"name": "Fido"}]
    assert load_animals(bad_json) == [{"name": "Rex"}]

    assert any("json decode error" in msg.message.lower() or "file not found" in msg.message.lower()
               for msg in caplog.records)


def test_save_rejects_invalid_data_structure(tmp_path, caplog):
    file_ = tmp_path / "invalid.json"
    caplog.clear()
    save_animals(file_, {"not": "a list"})
    assert "expected list of dictionaries" in caplog.text.lower()
    assert not file_.exists()


def test_replace_all_animals_overwrites_and_validates(tmp_json, tmp_path, caplog):
    good_data = [{"name": "Solo"}]
    replace_all_animals(tmp_json, good_data)
    assert json.loads(tmp_json.read_text()) == good_data

    bad_file = tmp_path / "bad.json"
    caplog.clear()
    replace_all_animals(bad_file, {"not": "a list"})
    assert "expected list of dictionaries" in caplog.text.lower()
    assert not bad_file.exists()


def test_replace_all_and_save_animals_handle_exceptions(tmp_path, monkeypatch, caplog):
    file_1 = tmp_path / "fail1.json"
    file_2 = tmp_path / "fail2.json"

    monkeypatch.setattr(json, "dump", lambda *a, **k: (_ for _ in ()).throw(TypeError("boom")))
    caplog.set_level(logging.ERROR)

    save_animals(file_1, [{"name": "Rex"}])
    replace_all_animals(file_2, [{"name": "Bo"}])

    assert any("failed to write" in msg.message.lower() for msg in caplog.records)
