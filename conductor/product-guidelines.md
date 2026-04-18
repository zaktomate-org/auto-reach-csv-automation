# Product Guidelines

## Prose Style
- **Concise & Direct:** Documentation, commit messages, and logs should be brief and actionable. Avoid filler and focus on the technical details and immediate results.

## Communication & Logging
- **User-Centric Warnings:** Prioritize reporting errors that require user action (e.g., "Missing unprocessed folder", "Invalid CSV format") rather than low-level technical stack traces. This ensures that non-technical users in sales and marketing can understand and address common issues.

## User Interaction (CLI)
- **Automation-Ready:** The tool should be designed to run in a non-interactive manner, making it suitable for scheduled tasks (cron jobs) and background automation. It should not require manual input during the cleaning and processing cycle.

## Naming & File Organization
- **Minimalist Naming:** Prefer short, functional names for both code variables and output files (e.g., `all.csv`, `rejects.csv`, `clean_name`). This maintains consistency with the existing project structure and keeps the file system clean.

## Design Principles
- **Data Integrity Over Speed:** While automation is the goal, the priority is to preserve as much original data as possible when cleaning. The cleaning logic should be conservative and only strip data that is confirmed as noise or punctuation.
- **Portability:** Keep the tech stack lightweight and standard-compliant to ensure the tool can be moved and run on different systems with minimal environment setup.
