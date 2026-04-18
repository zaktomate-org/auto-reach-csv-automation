import argparse
import sys
import cleaner

def parse_args(args):
    parser = argparse.ArgumentParser(description="Process CSV files for CRM synchronization.")
    parser.add_argument("--path", default="unprocessed", help="The directory to watch for incoming CSV files.")
    parser.add_argument("--url", help="The base URL for the CRM API (required if --crm is used).")
    parser.add_argument("--crm", action="store_true", help="Enable the CRM synchronization workflow.")
    parser.add_argument("--type", help="The value for the 'type' field in CRM entries.")
    parser.add_argument("--sentby", help="The value for the 'sentBy' field in CRM entries.")
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.crm:
        missing = []
        if not parsed_args.url:
            missing.append("--url")
        if not parsed_args.type:
            missing.append("--type")
        if not parsed_args.sentby:
            missing.append("--sentby")
        
        if missing:
            parser.error(f"the following arguments are required if --crm is set: {', '.join(missing)}")
            
    return parsed_args

def main():
    args = parse_args(sys.argv[1:])
    # For Phase 1, we only update the argument parsing.
    # We call cleaner.main() which will be refactored in subsequent steps.
    # Currently cleaner.main() takes its own sys.argv[1].
    # To maintain current behavior while refactoring, we can override sys.argv or refactor cleaner.py.
    # Refactoring cleaner.py is more robust.
    import cleaner
    cleaner.main_with_args(args)

if __name__ == "__main__":
    main()
