# Map - CSV Cleaning & CRM Sync Tool

A Python-based tool designed for sales and marketing teams to automate the cleaning, deduplication, and synchronization of company lead data from CSV files.

## Core Features

- **Dynamic Batch CSV Processing:** Automatically ingests CSV files from a user-specified directory.
- **CLI Flag Control:** Configurable execution using named flags for flexible processing.
- **Idempotent File Tracking:** Ensures each file is only processed once using a persistent tracking system.
- **Data Cleaning & Standardization:**
    - Standardizes company names by removing noise while preserving context.
    - Validates phone numbers (e.g., `+8801...` patterns) and strips formatting for consistency.
    - Preserves data integrity by only removing confirmed noise.
- **CRM Synchronization:** Optional automated sync of cleaned rows to an external CRM API with built-in retry logic (3 attempts).

## Tech Stack

- **Language:** Python (>= 3.12)
- **Data Processing:** `pandas`
- **Networking:** `requests`
- **Package Management:** `uv`
- **Testing:** `pytest` with `pytest-cov`

## Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd maps
   ```

2. Synchronize dependencies:
   ```bash
   uv sync
   ```

## Usage

Run the tool using `uv run python main.py`.

### Basic Cleaning

Process files from the default `unprocessed/` directory:
```bash
uv run python main.py
```

Process files from a custom directory:
```bash
uv run python main.py --path ./my_csvs
```

### CRM Synchronization

To enable CRM sync, provide the `--crm` flag along with the required API details:

```bash
uv run python main.py \
  --crm \
  --url "https://your-crm-api.com" \
  --type "lead" \
  --sentby "YourName"
```

**CRM Flags:**
- `--crm`: Enable the CRM synchronization workflow.
- `--url`: (Required with `--crm`) The base URL for the CRM API.
- `--type`: (Required with `--crm`) The `type` field value for CRM entries.
- `--sentby`: (Required with `--crm`) The `sentBy` field value for CRM entries.

## Project Structure

- `main.py`: Entry point for the CLI.
- `cleaner.py`: Core logic for CSV processing and validation.
- `crm_client.py`: API client for CRM integration.
- `processed_files.txt`: Persistent log of processed filenames.
- `all.csv`: Master archive of all ingested rows.
- `rejects.csv`: Log of rows that failed validation.

## Development

### Running Tests

Execute the full test suite (including unit and integration tests):
```bash
PYTHONPATH=. uv run pytest
```

### Coverage Report

Generate a coverage report:
```bash
PYTHONPATH=. uv run pytest --cov=main --cov=cleaner --cov=crm_client
```

## License

[Add License Information Here]
