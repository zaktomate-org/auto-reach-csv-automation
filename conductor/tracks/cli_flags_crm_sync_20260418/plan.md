# Implementation Plan: CLI Flag Refactoring & CRM Integration

This plan outlines the steps to refactor the CLI to use flags and implement a CRM synchronization workflow.

## Phase 1: CLI Refactoring [checkpoint: a365bac]
Refactor `main.py` to use `argparse` with named flags instead of positional arguments.

- [x] Task: Update Argument Parsing in main.py [0a8ee17]
    - [ ] Write tests for new argument parsing (flags and defaults)
    - [ ] Implement `argparse` with flags: `--path`, `--url`, `--crm`, `--type`, `--sentby`
    - [ ] Add validation logic to ensure CRM-related flags are present if `--crm` is set
    - [ ] Update any internal references to arguments
- [x] Task: Conductor - User Manual Verification 'Phase 1: CLI Refactoring' (Protocol in workflow.md) [a365bac]

## Phase 2: CRM Integration Module [checkpoint: 5329ea2]
Develop a dedicated module to handle communication with the CRM API.

- [x] Task: Create CRM Client Module [7133bf4]
    - [ ] Write tests for CRM "check" and "entry" API calls (mocking responses)
    - [ ] Write tests for the 3-retry logic and 12-hour time formatting
    - [ ] Implement `CRMClient` class with methods for `check_number` and `create_entry`
    - [ ] Implement 12-hour time formatting for the `sentIn` field
- [x] Task: Conductor - User Manual Verification 'Phase 2: CRM Integration Module' (Protocol in workflow.md) [5329ea2]

## Phase 3: Workflow Integration & Logging
Integrate the CRM module into the main processing loop and add detailed logging.

- [ ] Task: Integrate CRM Sync into Processing Flow
    - [ ] Write tests for the end-to-end sync flow using a mock CSV
    - [ ] Implement sequential row-by-row sync after a CSV is saved to `processed/`
    - [ ] Add console logging for sync status (Skip/Success/Failure)
    - [ ] Ensure the script remains resilient to individual row failures
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Integration and End-to-End Sync' (Protocol in workflow.md)
