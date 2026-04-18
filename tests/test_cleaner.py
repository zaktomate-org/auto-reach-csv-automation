import pytest
from pathlib import Path
from cleaner import setup_directories, get_input_files
import os

def test_get_input_files(tmp_path):
    # Setup: Create some files
    (tmp_path / "test1.csv").write_text("col1,col2\n1,2")
    (tmp_path / "test2.csv").write_text("col1,col2\n3,4")
    (tmp_path / "not_csv.txt").write_text("hello")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir/inner.csv").write_text("inner")
    
    files = get_input_files(tmp_path)
    
    filenames = [f.name for f in files]
    assert "test1.csv" in filenames
    assert "test2.csv" in filenames
    assert "not_csv.txt" not in filenames
    assert "inner.csv" not in filenames 
    assert len(files) == 2

def test_setup_directories_default(tmp_path, monkeypatch):
    # Setup: Create 'unprocessed' in tmp_path
    unprocessed = tmp_path / "unprocessed"
    unprocessed.mkdir()
    
    # Change CWD to tmp_path
    monkeypatch.chdir(tmp_path)
    
    inp, out = setup_directories()
    
    assert inp.name == "unprocessed"
    assert out.name == "processed"
    assert out.exists()

def test_setup_directories_custom(tmp_path, monkeypatch):
    # Setup: Create custom directory in tmp_path
    custom_dir = tmp_path / "my_input"
    custom_dir.mkdir()
    
    # Change CWD to tmp_path
    monkeypatch.chdir(tmp_path)
    
    # This should fail if setup_directories doesn't accept arguments
    inp, out = setup_directories("my_input")
    
    assert inp.name == "my_input"
    assert out.name == "processed"
    assert out.exists()

def test_setup_directories_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    # Should exit or raise error if folder doesn't exist
    with pytest.raises(SystemExit):
        setup_directories("non_existent")
