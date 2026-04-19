import pytest
from unittest.mock import patch, MagicMock
from crm_client import CRMClient
import pandas as pd
from cleaner import main_with_args
from pathlib import Path
import requests

# Create a mock object for args
class Args:
    path = "unprocessed"
    crm = True
    url = "http://test.com"
    type = "lead"
    sentby = "Gemini"

@patch("requests.request")
def test_crm_sync_integration_duplicate_skip(mock_request, tmp_path):
    # Setup CRM mock responses
    def request_side_effect(method, url, **kwargs):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        if method == "GET" and "api/check" in url:
            if "number=01712345678" in url:
                mock_resp.text = '"match"' # Quoted response
            else:
                mock_resp.text = '"not match"' # Quoted response
        elif method == "POST" and "api/entry" in url:
            mock_resp.text = '"OK"'
        return mock_resp
    
    mock_request.side_effect = request_side_effect
    
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
    
    args = Args()
    args.path = str(unprocessed_dir)
    
    with patch("cleaner.FileTracker") as mock_tracker_cls:
        mock_tracker = mock_tracker_cls.return_value
        mock_tracker.is_processed.return_value = False
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            main_with_args(args)
    
    # Should call check_number with "01712345678" which should return "match"
    # and should NOT call POST /api/entry.
    
    # Check GET calls
    check_calls = [c for c in mock_request.call_args_list if c.args[0] == "GET"]
    assert len(check_calls) == 1
    assert "number=01712345678" in check_calls[0].args[1]
    
    # Check POST calls
    post_calls = [c for c in mock_request.call_args_list if c.args[0] == "POST"]
    assert len(post_calls) == 0
