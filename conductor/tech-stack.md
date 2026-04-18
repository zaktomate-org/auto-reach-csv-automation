# Tech Stack

## Language & Runtime
- **Python (>= 3.12):** Used for the core logic, scripting, and data manipulation.

## Core Libraries
- **pandas:** The primary library for data manipulation, cleaning, and CSV processing. It provides high-performance, easy-to-use data structures.
- **requests:** Used for making HTTP requests to the CRM API for synchronization.
- **pathlib:** Used for modern, object-oriented filesystem path manipulation.
- **re (Regex):** Used for string cleaning and validation (e.g., phone numbers and company names).

## Tools & Package Management
- **uv:** A fast Python package installer and resolver, used for managing dependencies and the virtual environment.
- **pytest:** A mature, full-featured Python testing tool used for unit and integration testing.
- **pytest-cov:** A pytest plugin that produces coverage reports.

## Infrastructure & Deployment
- **Filesystem-based Processing:** The tool operates on local directories (`unprocessed`, `processed`) and CSV files, ensuring a zero-infrastructure footprint.
