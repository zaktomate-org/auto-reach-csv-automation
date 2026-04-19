import pytest
from unittest.mock import patch, MagicMock
from crm_client import CRMClient
import pandas as pd
from cleaner import main_with_args
from pathlib import Path

# Create a mock object for args
class Args:
    path = "unprocessed"
    crm = True
    url = "http://test.com"
    type = "lead"
    sentby = "Gemini"

@patch("crm_client.CRMClient.check_number")
@patch("crm_client.CRMClient.create_entry")
def test_crm_sync_duplicate_skip_with_dashes(mock_create, mock_check, tmp_path):
    # Create a real dummy CSV file
    unprocessed_dir = tmp_path / "unprocessed"
    unprocessed_dir.mkdir()
    csv_file = unprocessed_dir / "test.csv"
    
    # Input has dashes
    df = pd.DataFrame({
        'title': ['Company A'],
        'phone': ['01712-345678'],
        'website': ['http://a.com'],
        'link': ['l1'], 
        'category': ['c1'], 
        'address': ['a1'], 
        'timezone': ['Asia/Dhaka'], 
        'emails': ['e1']
    })
    df.to_csv(csv_file, index=False)
    
    # CRM check mock: returns True ONLY IF the number is exactly "01712345678" (no dashes)
    # If called with "01712-345678", it returns False (simulating CRM case sensitivity/strictness)
    def side_effect(phone):
        return phone == "01712345678"
    
    mock_check.side_effect = side_effect
    mock_create.return_value = True
    
    args = Args()
    args.path = str(unprocessed_dir)
    
    with patch("cleaner.FileTracker") as mock_tracker_cls:
        mock_tracker = mock_tracker_cls.return_value
        mock_tracker.is_processed.return_value = False
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            main_with_args(args)
    
    # If the logic is FLAWED, it will call check_number with "01712-345678"
    # which will return False, and then it will call create_entry.
    # We WANT it to call check_number with "01712345678" and thus SKIP create_entry.
    
    # Let's assert that create_entry was NOT called. 
    # If this test FAILS, it means we have reproduced the "duplicate added" issue.
    mock_create.assert_not_called()
