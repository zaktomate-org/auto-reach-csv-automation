# Product Definition

## Initial Concept
A Python-based tool for cleaning and deduplicating company data from CSV files.

## Target Audience
- **Sales Teams:** Marketing teams and sales professionals who need to manage and clean lead lists for various campaigns.

## Core Features
- **Batch CSV Processing:** Automated ingestion of CSV files from an `unprocessed` directory, processing them, and moving results to a `processed` directory.
- **Company Name Cleaning:** Standardizing company names by removing unnecessary punctuation and whitespace while maintaining a minimum character threshold to preserve context.
- **Phone Number Validation:** Identifying and validating specific phone number patterns (e.g., `+8801...`) to ensure data accuracy.

## Primary Goal
- **Workflow Automation:** The single most important goal is to automate the entire data cleaning workflow, from initial file ingestion to archiving and deduplication, to save time and reduce manual errors.

## Technical Constraints & Considerations
- **Data Integrity:** A primary constraint is to preserve as much original data as possible during the cleaning process to avoid losing valuable information.
- **Lightweight Footprint:** The tool should have minimal external dependencies (e.g., relying on standard libraries and `pandas`) to ensure easy deployment and portability.
