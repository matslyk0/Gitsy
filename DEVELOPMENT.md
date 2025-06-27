# Gitsy Development Guidelines

This document outlines the development standards and practices for the Gitsy project.

### Branching Strategy

Work must be done on feature branches. `main` is considered protected and changes must be merged via a pull request.

Follow this convention for naming branches:

`feature/<short-description>`
`fix/<short-description>`
`docs/<short-description>`

Example:

`feature/add-redis-caching`

### Commit Messages

Format:

`<type>: <subject>`

Example:

`fix: correct calculation for average pull request close time`

### Pull Requests

Feature branches must be merged into `main` with a pull request.
- The title should describe the changes.
- Use `.github/PULL_REQUEST_TEMPLATE.md` to provide a summary of the changes and outline how to test them.
- Check for code quality, adherence to standards, and ensure all tests pass.

### Coding Standards
- Python code will be formatted with `black` and linted with `flake8`. The CI pipeline will check for this automatically.
- JavaScript/React code will be formatted using `prettier`.

### Environment Variables
API keys and environment-specific configurations must be stored in a `.env` file and should never be committed to the repository. Consult the `.env.example` file in the `backend` directory to show the required variables.

### Testing
All new backend features should be accompanied by unit tests. Tests are run automatically via GitHub Actions on every push and pull request to the `main` branch.







