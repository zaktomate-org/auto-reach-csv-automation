import requests
import time
from datetime import datetime

class CRMClient:
    def __init__(self, base_url, crm_type, sent_by, debug=False):
        self.base_url = base_url.rstrip('/')
        self.crm_type = crm_type
        self.sent_by = sent_by
        self.debug = debug
        self.max_retries = 3
        self.retry_delay = 1  # second

    @staticmethod
    def normalize_phone(phone: str) -> str:
        """Normalize phone: remove .0 suffix, dashes, and whitespace."""
        phone = str(phone).strip()
        if phone.endswith('.0'):
            phone = phone[:-2]
        return phone.replace('-', '').replace(' ', '')

    def get_formatted_time(self):
        """Returns current system time in 12-hour format (e.g., '02:30 PM')."""
        return datetime.now().strftime("%I:%M %p")

    def _request_with_retry(self, method, url, **kwargs):
        for attempt in range(self.max_retries):
            try:
                response = requests.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if self.debug:
                    self._debug_error(method, url, kwargs, e)
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay)
        return None

    def _debug_error(self, method, url, kwargs, error):
        """Print debug info for failed requests."""
        print(f"  [DEBUG] ERROR Request: {method} {url}")
        if kwargs.get("json"):
            print(f"  [DEBUG] Request Body: {kwargs['json']}")
        print(f"  [DEBUG] Error: {error}")

    def _clean_field(self, value):
        """Clean field value: return empty string for None/nan/empty, otherwise strip whitespace."""
        if value is None:
            return ""
        val_str = str(value).strip()
        if val_str.lower() in ["", "nan", "none"]:
            return ""
        return val_str

    def check_number(self, phone):
        """
        Step A: Check Existing Entry
        Returns True if 'match', False if 'not match'.
        """
        phone = self.normalize_phone(phone)
        url = f"{self.base_url}/api/check?number={phone}"
        try:
            response = self._request_with_retry("GET", url)
            raw_text = response.text.strip()
            clean_text = raw_text.strip('"').lower()
            result = clean_text == "match"
            if self.debug and not result:
                print(f"  [DEBUG] Check failed: {phone} -> Raw: '{raw_text}'")
            return result
        except Exception as e:
            if self.debug:
                self._debug_error("GET", url, {}, e)
            raise e

    def create_entry(self, row):
        """
        Step B: Create New Entry
        """
        url = f"{self.base_url}/api/entry"
        phone = self.normalize_phone(row.get("phone", ""))
        data = {
            "company": self._clean_field(row.get("Company Name")),
            "whatsapp": phone,
            "type": self.crm_type,
            "website": self._clean_field(row.get("website")),
            "facebook": "",
            "sentBy": self.sent_by,
            "sentIn": self.get_formatted_time(),
            "messageSent": "no"
        }
        try:
            response = self._request_with_retry("POST", url, json=data)
            success = response.status_code == 200
            if not success:
                if self.debug:
                    self._debug_error("POST", url, {"json": data}, f"HTTP {response.status_code}: {response.text}")
                raise Exception(f"Failed to create entry: HTTP {response.status_code}")
            return success
        except Exception as e:
            if self.debug:
                self._debug_error("POST", url, {"json": data}, e)
            raise e

    def create_entry_no_phone(self, row):
        """Create entry when phone is empty (for valid timezone fallback)."""
        url = f"{self.base_url}/api/entry"
        data = {
            "company": self._clean_field(row.get("Company Name")),
            "whatsapp": "",
            "type": self.crm_type,
            "website": self._clean_field(row.get("website")),
            "facebook": "",
            "sentBy": self.sent_by,
            "sentIn": self.get_formatted_time(),
            "messageSent": "no"
        }
        try:
            response = self._request_with_retry("POST", url, json=data)
            success = response.status_code == 200
            if not success:
                if self.debug:
                    self._debug_error("POST", url, {"json": data}, f"HTTP {response.status_code}: {response.text}")
                raise Exception(f"Failed to create entry: HTTP {response.status_code}")
            return success
        except Exception as e:
            if self.debug:
                self._debug_error("POST", url, {"json": data}, e)
            raise e
