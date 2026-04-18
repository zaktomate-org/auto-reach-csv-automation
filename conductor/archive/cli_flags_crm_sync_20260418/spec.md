# Specification: CLI Flag Refactoring & CRM Integration

## Overview
This track involves two main objectives:
1. Refactoring the `main.py` entry point to use named flags (e.g., `--path`) instead of positional arguments for better usability.
2. Implementing an optional CRM integration workflow that syncs cleaned data to an external API.

## Functional Requirements

### 1. CLI Refactoring
- Replace positional arguments with the following flags:
    - `--path`: (Optional) The directory to watch for incoming CSV files. Defaults to `unprocessed/`.
    - `--url`: (Required if `--crm` is used) The base URL for the CRM API.
    - `--crm`: (Optional) A boolean flag to enable the CRM synchronization workflow.
    - `--type`: (Optional) The value for the `type` field in CRM entries.
    - `--sentby`: (Optional) The value for the `sentBy` field in CRM entries.
- The script should validate that if `--crm` is provided, `--url`, `--type`, and `--sentby` are also present.

### 2. CRM Synchronization Workflow
The CRM sync occurs **after** a CSV has been cleaned and saved to the `processed/` directory. For each row in the cleaned CSV, the following steps are performed sequentially:

#### Step A: Check Existing Entry
- **Endpoint**: `GET <base_url>/api/check?number=<phone>`
- **Logic**:
    - If the response is `"match"`, the row is skipped (already exists in CRM).
    - If the response is `"not match"`, the script proceeds to Step B.

#### Step B: Create New Entry
- **Endpoint**: `POST <base_url>/api/entry`
- **Request Body (JSON)**:
    - `company`: Taken from the `title` column of the CSV.
    - `whatsapp`: Taken from the `phone` column of the CSV.
    - `type`: Taken from the `--type` CLI flag.
    - `website`: Taken from the `website` column of the CSV.
    - `facebook`: Always empty string `""`.
    - `sentBy`: Taken from the `--sentby` CLI flag.
    - `sentIn`: Current system time in 12-hour format (e.g., `"02:30 PM"`).
    - `messageSent`: Always `"no"`.

### 3. Error Handling & Reliability
- **Retry Logic**: If an API request fails (network error or non-200 response), the script must retry up to 3 times with a brief delay.
- **Resilience**: If a row fails after all retries, log the error and move to the next row. Do not halt the entire process.
- **Sequence**: CRM sync must happen sequentially (one row at a time) to avoid overwhelming the API.

## Non-Functional Requirements
- **Logging**: Provide console output for each CRM action (e.g., "Skipping [Number]: Match found", "Created entry for [Company]").
- **Performance**: Ensure the cleaning logic remains fast; the CRM sync is the only part expected to be I/O bound.

## Acceptance Criteria
- Running `python main.py --path ./my_data` correctly processes the directory.
- Enabling `--crm` successfully checks and adds entries to the provided `--url`.
- `sentIn` field correctly reflects the local time in 12-hour format.
- Invalid flags or missing required flags for CRM mode trigger a clear error message.

## Out of Scope
- GUI implementation.
- Real-time file watching (polling or manual execution is sufficient).
- Advanced CRM field mapping (only fixed mappings defined above).
