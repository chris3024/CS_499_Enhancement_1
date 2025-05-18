import json
import logging
from data.data_manager import read_animal_data, append_animal_records, overwrite_animal_data


def test_read_returns_list(tmp_json):
    animals = read_animal_data(tmp_json)
    assert isinstance(animals, list)
    assert len(animals) == 4


def test_read_handles_missing_and_bad_json(tmp_path, caplog):
    missing = tmp_path / "missing.json"
    corrupt = tmp_path / "bad.json"
    not_list = tmp_path / "notlist.json"

    corrupt.write_text("{ bad json ]")
    not_list.write_text('{"key": "value"}')

    caplog.clear()
    assert read_animal_data(missing) == []
    assert read_animal_data(corrupt) == []
    assert read_animal_data(not_list) == []

    assert any("file not found" in msg.message.lower() or "failed to parse json" in msg.message.lower()
               for msg in caplog.records)


def test_append_adds_to_file(tmp_path):
    file_ = tmp_path / "dogs.json"
    append_animal_records(file_, [{"name": "Fido"}])
    append_animal_records(file_, [{"name": "Molly"}])
    names = {a["name"] for a in read_animal_data(file_)}
    assert names == {"Fido", "Molly"}


def test_append_recovers_from_invalid_or_nonlist_files(tmp_path, caplog):
    not_list = tmp_path / "notlist.json"
    bad_json = tmp_path / "bad.json"

    not_list.write_text('{"oops": 1}')
    bad_json.write_text("{ bad json ]")

    caplog.clear()
    append_animal_records(not_list, [{"name": "Fido"}])
    append_animal_records(bad_json, [{"name": "Rex"}])

    assert read_animal_data(not_list) == [{"name": "Fido"}]
    assert read_animal_data(bad_json) == [{"name": "Rex"}]

    assert any("failed to parse json" in msg.message.lower() or "file not found" in msg.message.lower()
               for msg in caplog.records)


def test_append_rejects_invalid_structure(tmp_path, caplog):
    file_ = tmp_path / "invalid.json"
    caplog.clear()
    append_animal_records(file_, {"not": "a list"})
    assert "expected list of dictionaries" in caplog.text.lower()
    assert not file_.exists()


def test_overwrite_overwrites_and_validates(tmp_json, tmp_path, caplog):
    good_data = [{"name": "Solo"}]
    overwrite_animal_data(tmp_json, good_data)
    assert json.loads(tmp_json.read_text()) == good_data

    bad_file = tmp_path / "bad.json"
    caplog.clear()
    overwrite_animal_data(bad_file, {"not": "a list"})
    assert "expected list of dictionaries" in caplog.text.lower()
    assert not bad_file.exists()


def test_overwrite_and_append_handle_exceptions(tmp_path, monkeypatch, caplog):
    file_1 = tmp_path / "fail1.json"
    file_2 = tmp_path / "fail2.json"

    monkeypatch.setattr(json, "dump", lambda *a, **k: (_ for _ in ()).throw(TypeError("boom")))
    caplog.set_level(logging.ERROR)

    append_animal_records(file_1, [{"name": "Rex"}])
    overwrite_animal_data(file_2, [{"name": "Bo"}])

    assert any("could not write to file" in msg.message.lower() or "failed to write" in msg.message.lower()
               for msg in caplog.records)
