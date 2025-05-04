from data.data_manager import load_animals, save_animals, replace_all_animals
import json

def test_load_returns_list(tmp_json):
    animals = load_animals(tmp_json)
    assert isinstance(animals, list)
    assert len(animals) == 4

def test_load_missing_file_returns_empty(tmp_path):
    missing = tmp_path / "nowhere.json"
    assert load_animals(missing) == []

def test_save_appends(tmp_path):
    file = tmp_path / "dogs.json"
    first = [{"name": "Fido"}]
    save_animals(file, first)
    assert load_animals(file) == first

    second = [{"name": "Molly"}]
    save_animals(file, second)
    combined = load_animals(file)
    assert len(combined) == 2
    names = [a["name"] for a in combined]
    assert {"Fido", "Molly"} <= set(names)

def test_replace_overwrites(tmp_json):
    new = [{"name": "OnlyOne"}]
    replace_all_animals(tmp_json, new)
    animals = json.loads(tmp_json.read_text())
    assert animals == new
