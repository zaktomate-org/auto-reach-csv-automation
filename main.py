"""Main entry point for the map project."""
import argparse
import sys

import cleaner


def parse_args(args):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Process CSV files for CRM synchronization."
    )
    parser.add_argument(
        "--path", default="unprocessed",
        help="The directory to watch for incoming CSV files."
    )
    parser.add_argument(
        "--url",
        help="The base URL for the CRM API (required if --crm is used)."
    )
    parser.add_argument(
        "--crm", action="store_true",
        help="Enable the CRM synchronization workflow."
    )
    parser.add_argument(
        "--type",
        help="The value for the 'type' field in CRM entries."
    )
    parser.add_argument(
        "--sentby",
        help="The value for the 'sentBy' field in CRM entries."
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable debug mode to show full request/response on errors."
    )
    
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
            parser.error(
                f"the following arguments are required if --crm is set: "
                f"{', '.join(missing)}"
            )
            
    return parsed_args


def main():
    """Main entry point."""
    args = parse_args(sys.argv[1:])
    cleaner.main_with_args(args)

if __name__ == "__main__":
    main()
