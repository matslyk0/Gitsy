### Branching Strategy

Work must be done on feature branches named `{feature, fix, docs}/<short-description>`. `main` is considered protected and changes must be merged via a pull request, with exception to minor doc changes.

### Commit Messages

Follow this convention for commit messages `{feature, fix, docs}: <short-description>`. A commit description is encouraged if the commit title is not self-explanatory.

### Pull Requests

- Rename pull requests close to whatever the generated title is.
- `.github/PULL_REQUEST_TEMPLATE.md` will provide a template for you to fill in.
- Remember to attach issues, assignees, labels and the Kanban board `Core`.

### Coding Standards
- Python code will be formatted with `black` and linted with `flake8`. 
- JavaScript/React code will be formatted using `prettier` and linted with `eslint`.
- The CI pipeline will check for this automatically when it is implemented.

### Environment Variables
API keys and environment-specific configurations must be stored in a `.env` file and should never be committed to the repository. Consult the `.env.example` file in the root directory to show the required variables. For the large majority of testing, you will need to generate your own GitHub personal access token (classic, not fine-grained) which has a rate limit of 5000 per hour. The non-token rate limit for the GitHub API is 60 per hour, which will gas out for any normal sized repository. 

To create your own token, follow these steps:
- On GitHub, go to `Profile` -> `Settings` -> `Developer settings`,
- Click the drop-down on `Personal access tokens`,
- Click `Tokens (classic)`,
- Click the drop-down on `Generate new token` and select `Generate new token (classic)`,
- Follow the steps then copy the token into your `.env` file as shown in `.env.example`.

### Testing
All new backend features should be accompanied by unit tests. If unit tests are not applicable, please instead provide steps to recreate how you tested. Tests will later be run automatically via GitHub Actions on every push and pull request to `main`.
