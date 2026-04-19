import requests
import time
from datetime import datetime

class CRMClient:
    def __init__(self, base_url, crm_type, sent_by):
        self.base_url = base_url.rstrip('/')
        self.crm_type = crm_type
        self.sent_by = sent_by
        self.max_retries = 3
        self.retry_delay = 1 # second

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
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay)
        return None

    def check_number(self, phone):
        """
        Step A: Check Existing Entry
        Returns True if 'match', False if 'not match'.
        """
        url = f"{self.base_url}/api/check?number={phone}"
        print(f"CRM_CLIENT: Checking number {phone} at {url}")
        try:
            response = self._request_with_retry("GET", url)
            # Strip whitespace and literal double quotes from the response
            raw_text = response.text.strip()
            clean_text = raw_text.strip('"').lower()
            result = clean_text == "match"
            print(f"CRM_CLIENT: Check result for {phone}: {result} (Raw: '{raw_text}', Cleaned: '{clean_text}')")
            return result
        except Exception as e:
            print(f"CRM_CLIENT: Error checking number {phone}: {e}")
            raise e

    def create_entry(self, row):
        """
        Step B: Create New Entry
        """
        url = f"{self.base_url}/api/entry"
        phone = row.get("phone", "")
        data = {
            "company": row.get("Company Name", ""),
            "whatsapp": phone,
            "type": self.crm_type,
            "website": row.get("website", ""),
            "facebook": "",
            "sentBy": self.sent_by,
            "sentIn": self.get_formatted_time(),
            "messageSent": "no"
        }
        print(f"CRM_CLIENT: Creating entry for {row.get('Company Name')} ({phone}) at {url}")
        try:
            response = self._request_with_retry("POST", url, json=data)
            success = response.status_code == 200
            print(f"CRM_CLIENT: Creation {'succeeded' if success else 'failed'} for {phone} (Status: {response.status_code})")
            return success
        except Exception as e:
            print(f"CRM_CLIENT: Error creating entry for {phone}: {e}")
            raise e
