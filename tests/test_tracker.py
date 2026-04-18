import pytest
from pathlib import Path
from cleaner import FileTracker, main
import os
from unittest.mock import patch, MagicMock

# ... existing tests ...

def test_main_skips_processed_files(tmp_path, monkeypatch):
    # Setup directories
    unprocessed = tmp_path / "unprocessed"
    unprocessed.mkdir()
    processed = tmp_path / "processed"
    processed.mkdir()
    
    # Create input files
    file1 = unprocessed / "file1.csv"
    file1.write_text("Company Name,phone,website\nTest1,01711-123456,test1.com")
    file2 = unprocessed / "file2.csv"
    file2.write_text("Company Name,phone,website\nTest2,01711-654321,test2.com")
    
    # Create tracker and pre-mark file1 as processed
    tracker_path = tmp_path / "processed_files.txt"
    tracker_path.write_text("file1.csv\n")
    
    # Mocking environment
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["cleaner.py", "unprocessed"])
    
    # Run main - we need to ensure it uses our tracker_path
    # Since tracker_path is hardcoded in main (we need to decide where it lives)
    # Let's assume for now it lives in Path.cwd() / 'processed_files.txt'
    
    with patch("pandas.read_csv") as mock_read:
        # Mocking to avoid actual processing issues in this test
        mock_read.return_value = MagicMock()
        main()
        
        # Should only call read_csv for file2.csv
        # Actually, pandas might be used for other things, so let's check the calls
        called_files = [call.args[0].name for call in mock_read.call_args_list if hasattr(call.args[0], 'name')]
        assert "file1.csv" not in called_files
        assert "file2.csv" in called_files

def test_tracker_init(tmp_path):
    tracker_path = tmp_path / "tracker.txt"
    tracker = FileTracker(tracker_path)
    assert tracker.path == tracker_path
    assert tracker.processed_files == set()

def test_tracker_add_and_contains(tmp_path):
    tracker_path = tmp_path / "tracker.txt"
    tracker = FileTracker(tracker_path)
    
    tracker.add("file1.csv")
    assert tracker.is_processed("file1.csv")
    assert not tracker.is_processed("file2.csv")

def test_tracker_persistence(tmp_path):
    tracker_path = tmp_path / "tracker.txt"
    tracker = FileTracker(tracker_path)
    tracker.add("file1.csv")
    tracker.add("file2.csv")
    
    # New tracker instance with same path should load existing data
    tracker2 = FileTracker(tracker_path)
    assert tracker2.is_processed("file1.csv")
    assert tracker2.is_processed("file2.csv")
    assert len(tracker2.processed_files) == 2
