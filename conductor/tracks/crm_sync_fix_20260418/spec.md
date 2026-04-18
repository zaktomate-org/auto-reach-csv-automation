# Specification: Fix CRM Sync Duplicate Entries

## Overview
The CRM synchronization process is not correctly identifying or skipping existing phone numbers, leading to duplicate entries in the CRM, despite the `crm_client.check_number` logic being present in `cleaner.py`.

## Functional Requirements
- Improve logging during the CRM synchronization process to verify `check_number` is being called and responding correctly.
- Ensure that the synchronization logic actually checks for the existence of the phone number before adding the entry.
- Create a test case that reproduces the scenario where a duplicate is added, ensuring the fix is verified.

## Acceptance Criteria
- Logs should clearly indicate when a phone number is checked against the CRM.
- The `cleaner.py` script must correctly skip phone numbers that already exist in the CRM.
- A new automated test case demonstrates that `crm_client.check_number` is called and handled appropriately.

## Out of Scope
- Major architectural changes to the CRM sync logic (e.g., batch processing).
