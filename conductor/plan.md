# Implementation Plan: Implement dynamic folder processing with file tracking

## Phase 1: Core Logic Enhancements

- [x] Task: Implement Dynamic Folder Selection (c5304ed)
    - [ ] Write Tests: Verify script can accept and validate custom folder names
    - [ ] Implement Feature: Update `setup_directories` to use dynamic input
- [x] Task: Implement File Filtering (1478592)
    - [ ] Write Tests: Verify only `.csv` files are selected for processing
    - [ ] Implement Feature: Refine globbing/filtering logic in `main` loop
- [ ] Task: Conductor - User Manual Verification 'Core Logic Enhancements' (Protocol in workflow.md)

## Phase 2: File Tracking System

- [ ] Task: Implement Tracker Persistence
    - [ ] Write Tests: Verify tracker file is created and reads/writes correctly
    - [ ] Implement Feature: Create `Tracker` class or helper functions for I/O
- [ ] Task: Integrate Tracking into Processing Loop
    - [ ] Write Tests: Verify files already in tracker are skipped
    - [ ] Implement Feature: Update `main` to check and update tracker
- [ ] Task: Conductor - User Manual Verification 'File Tracking System' (Protocol in workflow.md)
