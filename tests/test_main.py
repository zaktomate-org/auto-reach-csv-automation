import pytest
import sys
from main import parse_args

def test_parse_args_default():
    args = parse_args([])
    assert args.path == 'unprocessed'
    assert args.crm is False
    assert args.url is None
    assert args.type is None
    assert args.sentby is None

def test_parse_args_custom_path():
    args = parse_args(['--path', 'custom_folder'])
    assert args.path == 'custom_folder'

def test_parse_args_crm_enabled():
    args = parse_args(['--crm', '--url', 'http://api.com', '--type', 'lead', '--sentby', 'Gemini'])
    assert args.crm is True
    assert args.url == 'http://api.com'
    assert args.type == 'lead'
    assert args.sentby == 'Gemini'

def test_parse_args_crm_missing_required():
    # If --crm is set, --url, --type, and --sentby are required
    with pytest.raises(SystemExit):
        parse_args(['--crm', '--url', 'http://api.com'])

def test_parse_args_crm_missing_url():
    with pytest.raises(SystemExit):
        parse_args(['--crm', '--type', 'lead', '--sentby', 'Gemini'])

def test_parse_args_crm_missing_type():
    with pytest.raises(SystemExit):
        parse_args(['--crm', '--url', 'http://api.com', '--sentby', 'Gemini'])

def test_parse_args_crm_missing_sentby():
    with pytest.raises(SystemExit):
        parse_args(['--crm', '--url', 'http://api.com', '--type', 'lead'])
