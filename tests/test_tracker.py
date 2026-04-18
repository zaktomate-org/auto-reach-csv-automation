import pytest
from pathlib import Path
from cleaner import FileTracker

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
