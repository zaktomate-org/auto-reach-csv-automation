# Specification: Implement dynamic folder processing with file tracking

## Objective
Enhance the data cleaning tool to support dynamic input folder selection and implement a tracking mechanism to prevent redundant processing of the same files.

## Scope
- **Dynamic Folder Selection:** Allow the user to specify the input directory name instead of hardcoding 'unprocessed'.
- **File Tracking System:** Create and maintain a tracker file (e.g., `processed_files.log` or a JSON equivalent) to record the names (or hashes) of files already processed.
- **Improved File Filtering:** Ensure the tool only processes `.csv` files and ignores all other file types in the source directory.

## Functional Requirements
1. **Dynamic Input:** The script should be able to accept a directory path or name as an argument or configuration.
2. **Persistence:** The tracker must persist between runs.
3. **Idempotency:** Re-running the script on the same folder should only process new or modified files.
4. **Validation:** Ensure the provided folder exists and is readable.

## Non-Functional Requirements
- **Performance:** Tracking should not significantly slow down the processing of large batches.
- **Reliability:** The tracker file should be updated only after a file is successfully processed and moved/archived.
- **Simplicity:** The solution should align with the project's "Lightweight Footprint" constraint.

## Technical Design
- **Configuration:** Use a simple variable or argument for the folder name.
- **Tracker Implementation:** A simple text file or JSON file stored in the root or `conductor` directory.
- **Processing Logic:** 
    1. Scan target directory for `*.csv`.
    2. Check each file against the tracker.
    3. Process only untracked files.
    4. Update tracker upon success.
