import pytest
from unittest.mock import patch, MagicMock
from crm_client import CRMClient
import requests
from datetime import datetime

@pytest.fixture
def client():
    return CRMClient(base_url="http://test.com", crm_type="lead", sent_by="Gemini")

def test_time_formatting(client):
    # Test 12-hour format: e.g., "02:30 PM"
    formatted_time = client.get_formatted_time()
    # Regex for 12-hour format with AM/PM
    import re
    assert re.match(r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$", formatted_time)

@patch("requests.request")
def test_check_number_match_quoted(mock_request, client):
    mock_request.return_value.status_code = 200
    mock_request.return_value.text = '"match"'  # Simulated JSON quoted response
    
    assert client.check_number("01712345678") is True
    mock_request.assert_called_once_with("GET", "http://test.com/api/check?number=01712345678")

@patch("requests.request")
def test_check_number_not_match(mock_request, client):
    mock_request.return_value.status_code = 200
    mock_request.return_value.text = '"not match"' # Simulated JSON quoted response
    
    assert client.check_number("01712345678") is False

@patch("requests.request")
def test_create_entry_success(mock_request, client):
    mock_request.return_value.status_code = 200
    
    row = {
        "Company Name": "Test Co",
        "phone": "01712345678",
        "website": "http://testco.com"
    }
    
    with patch.object(client, 'get_formatted_time', return_value="02:30 PM"):
        assert client.create_entry(row) is True
    
    expected_data = {
        "company": "Test Co",
        "whatsapp": "01712345678",
        "type": "lead",
        "website": "http://testco.com",
        "facebook": "",
        "sentBy": "Gemini",
        "sentIn": "02:30 PM",
        "messageSent": "no"
    }
    mock_request.assert_called_once_with("POST", "http://test.com/api/entry", json=expected_data)

@patch("requests.request")
def test_retry_logic_failure_then_success(mock_request, client):
    # First two fail, third succeeds
    mock_request.side_effect = [
        requests.exceptions.RequestException("Fail"),
        requests.exceptions.RequestException("Fail"),
        MagicMock(status_code=200, text="not match")
    ]
    
    # We should mock time.sleep to speed up tests
    with patch("time.sleep"):
        assert client.check_number("01712345678") is False
        assert mock_request.call_count == 3

@patch("requests.request")
def test_retry_logic_all_fail(mock_request, client):
    mock_request.side_effect = requests.exceptions.RequestException("Fail")
    
    with patch("time.sleep"):
        with pytest.raises(requests.exceptions.RequestException):
            client.check_number("01712345678")
        assert mock_request.call_count == 3
