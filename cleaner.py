import os
import re
import sys
import string
from pathlib import Path
import pandas as pd
from crm_client import CRMClient

def setup_directories(input_folder: str = 'unprocessed') -> tuple[Path, Path]:
    """Ensures input and output directories exist."""
    cwd = Path.cwd()
    unprocessed_dir = cwd / input_folder
    processed_dir = cwd / 'processed'
    
    # Environment Check
    if not unprocessed_dir.exists() or not unprocessed_dir.is_dir():
        print(f"Error: '{input_folder}' directory not found at {unprocessed_dir}")
        print("Please create it and add your input CSV files.")
        sys.exit(1)
        
    # Create processed directory if necessary
    processed_dir.mkdir(exist_ok=True)
    return unprocessed_dir, processed_dir

def get_input_files(input_dir: Path) -> list[Path]:
    """Returns a list of CSV files to process."""
    return [f for f in input_dir.glob('*.csv') if f.is_file()]

class FileTracker:
    """Tracks processed files to avoid redundant work."""
    def __init__(self, tracker_path: Path):
        self.path = tracker_path
        self.processed_files = self._load()

    def _load(self) -> set[str]:
        if not self.path.exists():
            return set()
        with open(self.path, 'r') as f:
            return {line.strip() for line in f if line.strip()}

    def _save(self):
        with open(self.path, 'w') as f:
            for filename in sorted(self.processed_files):
                f.write(f"{filename}\n")

    def is_processed(self, filename: str) -> bool:
        return filename in self.processed_files

    def add(self, filename: str):
        self.processed_files.add(filename)
        self._save()


class SyncedFileTracker:
    """Tracks files that have been fully synced to CRM."""
    def __init__(self, tracker_path: Path):
        self.path = tracker_path
        self.synced_files = self._load()

    def _load(self) -> set[str]:
        if not self.path.exists():
            return set()
        with open(self.path, 'r') as f:
            return {line.strip() for line in f if line.strip()}

    def _save(self):
        with open(self.path, 'w') as f:
            for filename in sorted(self.synced_files):
                f.write(f"{filename}\n")

    def is_synced(self, filename: str) -> bool:
        return filename in self.synced_files

    def add_synced(self, filename: str):
        self.synced_files.add(filename)
        self._save()


def run_crm_sync(final_df: pd.DataFrame, crm_client: CRMClient) -> bool:
    """Runs CRM sync for all rows. Returns True only if ALL rows complete successfully."""
    total = len(final_df)
    success_count = 0
    debug = crm_client.debug

    for index, row in final_df.iterrows():
        phone = str(row['phone']).strip()
        if phone.endswith('.0'):
            phone = phone[:-2]
        phone_missing = not phone or phone.lower() in ['nan', 'none', '']

        if phone_missing:
            try:
                if crm_client.create_entry_no_phone(row):
                    if not debug:
                        print(f"  Created entry (no phone) for {row['Company Name']}")
                    success_count += 1
                else:
                    print(f"  ERROR: Failed to create entry for {row['Company Name']} (no phone)")
            except Exception as e:
                print(f"  ERROR: Syncing row {index} (no phone): {e}")
            continue

        try:
            if crm_client.check_number(phone):
                if not debug:
                    print(f"  Skipping {phone}: Match found in CRM")
                success_count += 1
                continue

            if crm_client.create_entry(row):
                if not debug:
                    print(f"  Created entry for {row['Company Name']} ({phone})")
                success_count += 1
            else:
                print(f"  ERROR: Failed to create entry for {row['Company Name']} ({phone})")

        except Exception as e:
            print(f"  ERROR: Syncing row {index} ({phone}): {e}")

    return success_count == total

def clean_company_name(name: str) -> str:
    """
    Trims the company name and removes all characters following (and including) 
    the first instance of ANY punctuation (including unicode typography). 
    If the resulting string length is <= 3, reverts to the original name.
    """
    if pd.isna(name):
        return ""
    
    original_name = str(name).strip()
    
    # Combine standard ASCII punctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
    # with common web Unicode variants (en-dash, em-dash, and various vertical pipes)
    extended_punctuation = string.punctuation + "–—│┃｜"
    
    # Create a safe regex character class
    punct_pattern = r'[' + re.escape(extended_punctuation) + r']'
    
    # Split on the first occurrence of any punctuation
    cleaned_name = re.split(punct_pattern, original_name)[0].strip()
    
    # Revert to the original name if the trimmed result is 3 characters or shorter (or empty)
    if len(cleaned_name) <= 3:
        return original_name
        
    return cleaned_name

def append_to_csv(df: pd.DataFrame, path: Path):
    """Appends a dataframe to a CSV file."""
    if df.empty:
        return
    header = not path.exists()
    df.to_csv(path, mode='a', index=False, header=header)

def append_rejects(df: pd.DataFrame, path: Path):
    """Appends rejects to a central log, ensuring no global duplicates are introduced."""
    if df.empty:
        return
    if path.exists():
        try:
            # Read existing rejects to prevent cross-run duplicates
            existing_df = pd.read_csv(path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates()
            combined_df.to_csv(path, index=False)
        except Exception as e:
            print(f"Warning: Could not deduplicate against {path.name} cleanly (Error: {e}). Fallback to standard append.")
            df.drop_duplicates().to_csv(path, mode='a', index=False, header=False)
    else:
        df.drop_duplicates().to_csv(path, index=False)

def main_with_args(args):
    # Allow dynamic input folder from command line via argparse path
    input_folder = args.path
    unprocessed_dir, processed_dir = setup_directories(input_folder)
    
    root_dir = Path.cwd()
    master_all_path = root_dir / 'all.csv'
    master_rejects_path = root_dir / 'rejects.csv'
    tracker_path = root_dir / 'processed_files.txt'
    synced_tracker_path = root_dir / 'synced_files.txt'
    
    tracker = FileTracker(tracker_path)
    synced_tracker = SyncedFileTracker(synced_tracker_path)
    
    # Columns requested for Master / Rejects archive
    log_cols =['link', 'title', 'category', 'address', 'website', 'phone', 'timezone', 'emails']
    
    # Regex pattern: optionally starts with +88 or +880 (the `(?:\+88)?01` covers both), 
    # then 3 digits, an optional dash, and 6 digits.
    phone_pattern = r'^(?:\+88)?01\d{3}-?\d{6}$'

    for filepath in get_input_files(unprocessed_dir):
        filename = filepath.name
        
        if synced_tracker.is_synced(filename):
            print(f"Skipping {filename}: already cleaned and fully synced")
            continue
        
        crm_enabled = hasattr(args, 'crm') and args.crm
        
        if tracker.is_processed(filename):
            if not crm_enabled:
                print(f"Skipping {filename}: already processed (use --crm to sync)")
                continue
            print(f"Resuming CRM sync for {filename}...")
            final_df = pd.read_csv(processed_dir / filename)
            
            if crm_enabled:
                crm_client = CRMClient(args.url, args.type, args.sentby, debug=args.debug)
                sync_success = run_crm_sync(final_df, crm_client)
                if sync_success:
                    synced_tracker.add_synced(filename)
                    print(f"CRM sync complete for {filename}.")
                else:
                    print(f"CRM sync incomplete for {filename}. Will retry on next run.")
            continue
            
        try:
            df = pd.read_csv(filepath, dtype={'phone': str})
        except pd.errors.EmptyDataError:
            tracker.add(filepath.name)
            continue  # Gracefully skip completely empty files
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")
            continue

        if df.empty:
            tracker.add(filepath.name)
            continue

        # ---------------------------------------------------------
        # Step 3.1: Deduplication (Execute Before Processing)
        # ---------------------------------------------------------
        df = df.drop_duplicates()

        # Ensure all required columns exist natively to prevent KeyErrors
        for col in log_cols:
            if col not in df.columns:
                df[col] = pd.NA

        # ---------------------------------------------------------
        # Step 5.3: Master Archive Logging
        # ---------------------------------------------------------
        # Append every row (before any validation filters)
        all_log_df = df[log_cols].copy()
        append_to_csv(all_log_df, master_all_path)

        # ---------------------------------------------------------
        # Step 3.2: Filtering Logic (Validation & Rejection)
        # ---------------------------------------------------------
        # Strip all whitespace and dashes from phones so matching is highly robust
        phone_series = df['phone'].astype(str).str.strip().str.replace(r'[\s\-]+', '', regex=True)
        
        # Check if phone is genuinely null/empty
        phone_is_empty = df['phone'].isna() | phone_series.str.lower().isin(['', 'nan', 'none', '<na>'])
        
        # Validation checks
        valid_phone = phone_series.str.match(phone_pattern)
        valid_timezone = df['timezone'] == 'Asia/Dhaka'
        
        # Sequential Logic Application:
        # Keep row if Phone is Valid OR (Phone is strictly empty AND Timezone is valid)
        is_valid = valid_phone | (phone_is_empty & valid_timezone)
        
        valid_df = df[is_valid].copy()
        rejects_df = df[~is_valid].copy()

        # ---------------------------------------------------------
        # Step 5.2: Rejects Logging
        # ---------------------------------------------------------
        if not rejects_df.empty:
            rejects_log_df = rejects_df[log_cols].copy()
            append_rejects(rejects_log_df, master_rejects_path)

        # ---------------------------------------------------------
        # Step 4: Data Transformation
        # ---------------------------------------------------------
        if 'title' in valid_df.columns:
            valid_df = valid_df.rename(columns={'title': 'Company Name'})
        else:
            valid_df['Company Name'] = ''

        # Clean Company Name
        valid_df['Company Name'] = valid_df['Company Name'].apply(clean_company_name)
        
        # Standardize Phone Numbers (Remove dashes and whitespace)
        # We ensure they are strings first.
        valid_df['phone'] = valid_df['phone'].astype(str).str.strip().str.replace(r'[\s\-]+', '', regex=True)
        # Revert nan strings to empty
        valid_df['phone'] = valid_df['phone'].replace(['nan', 'None', '<NA>'], '')

        # Ensure all required final output columns are present
        for out_col in['Company Name', 'phone', 'website']:
            if out_col not in valid_df.columns:
                valid_df[out_col] = ''

        # Select and enforce column ordering
        final_df = valid_df[['Company Name', 'phone', 'website']]

        # ---------------------------------------------------------
        # Step 5.1: Processed Files Output
        # ---------------------------------------------------------
        output_filepath = processed_dir / filepath.name
        final_df.to_csv(output_filepath, index=False)
        tracker.add(filepath.name)
        print(f"Successfully processed: {filepath.name} (Kept {len(final_df)} / Rejected {len(rejects_df)})")

        # ---------------------------------------------------------
        # Phase 3: CRM Synchronization (Conditional)
        # ---------------------------------------------------------
        if crm_enabled:
            crm_client = CRMClient(args.url, args.type, args.sentby, debug=args.debug)
            print(f"Starting CRM sync for {filename}...")
            
            sync_success = run_crm_sync(final_df, crm_client)
            
            if sync_success:
                synced_tracker.add_synced(filename)
                print(f"CRM sync complete for {filename}.")
            else:
                print(f"CRM sync incomplete for {filename}. Will retry on next run.")

def main():
    # Allow dynamic input folder from command line
    input_folder = sys.argv[1] if len(sys.argv) > 1 else 'unprocessed'
    
    class Args:
        pass
    args = Args()
    args.path = input_folder
    main_with_args(args)

if __name__ == "__main__":
    main()
