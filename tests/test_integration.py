import pytest
import pandas as pd
from pathlib import Path
from cleaner import main_with_args
from unittest.mock import patch, MagicMock

@pytest.fixture
def setup_csv(tmp_path):
    unprocessed = tmp_path / "unprocessed"
    unprocessed.mkdir()
    processed = tmp_path / "processed"
    processed.mkdir()
    
    # Create a test CSV
    df = pd.DataFrame({
        "title": ["Company A", "Company B"],
        "phone": ["01712345678", "01812345678"],
        "timezone": ["Asia/Dhaka", "Asia/Dhaka"],
        "website": ["http://a.com", "http://b.com"]
    })
    csv_path = unprocessed / "test.csv"
    df.to_csv(csv_path, index=False)
    return tmp_path, csv_path

@patch("crm_client.CRMClient.check_number")
@patch("crm_client.CRMClient.create_entry")
def test_integration_crm_flow(mock_create, mock_check, setup_csv, monkeypatch):
    tmp_path, csv_path = setup_csv
    monkeypatch.chdir(tmp_path)
    
    # Mock behavior: 
    # Company A: Not in CRM (not match) -> Create entry
    # Company B: In CRM (match) -> Skip
    mock_check.side_effect = [False, True]
    mock_create.return_value = True
    
    class Args:
        path = "unprocessed"
        crm = True
        url = "http://api.com"
        type = "lead"
        sentby = "Gemini"
    
    main_with_args(Args())
    
    # Verify CRM client was called correctly
    assert mock_check.call_count == 2
    assert mock_create.call_count == 1
    
    # Check created entry was for Company A
    args, kwargs = mock_create.call_args
    row = args[0]
    assert row["Company Name"] == "Company A"
    assert row["phone"] == "01712345678"
    
    # Verify processed file exists
    processed_file = tmp_path / "processed" / "test.csv"
    assert processed_file.exists()
    processed_df = pd.read_csv(processed_file)
    assert len(processed_df) == 2

