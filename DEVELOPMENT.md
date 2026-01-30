### Branches
All work must be done on feature branches named `{feature, fix, docs}/<short-description>`, then merged to `main`. An exception is applicable to minor doc changes or CI/CD fixes.

### Commits
Commits should me named `{feature, fix, docs}: <short-description>` and a description is encouraged if the title is not self-explanatory or added context is needed.

### Pull Requests
`PULL_REQUEST_TEMPLATE.md` will provide a template for you to fill in. Attach issues, assignees, labels and the Kanban board `Gitsy`. Rename the title to fit the formatting of previous pull requests.

### Formatting and Linting
Python is formatted with `black` and linted with `flake8`. ReactJS is formatted with `prettier` and linted with `eslint`. Config files for both linters are included, but further setup depends on your IDE. 

The errors that linters spot are caught by automated tests and your IDE, and the other 'housekeeping' concerns are not critical. For this reason, the CI does not lint your code.

### Testing
To run tests, refer to `.github/workflows/ci.yml` and replicate the last 3 commands. The CI will automatically run all tests on a pull request, but running all tests before opening a pull request is recommended. The testing environment in the CI and in local development is identical, so a failed local test will also fail in the CI.

All new backend features should be accompanied by unit/integration tests in the `tests` folder. If such tests are not applicable to your change, provide a small guide to recreate your manual testing. 

### Environment Variables and GitHub Secrets
Consult `.env.example` for a list of environment variables to set up. The .gitignore includes `.env` for your peace of mind. All other environment variables are stored in GitHub Secrets (Actions) and are pulled via GitHub Actions in the CI/CD and pushed into the production environment.

The full list of Secrets is as follows:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `EC2_HOST`
- `EC2_SSH_KEY`
- `GIT_HUB_TOKEN` (can be the same as in `.env`)
- `POSTGRES_PROD_DB`
- `POSTGRES_PROD_PASSWORD`
- `POSTGRES_PROD_USER`.

### Setting up a GitHub Token
The unauthenticated rate limit for the GitHub API is 60 requests per hour, which won't get you anywhere beyond small repositories. The backend natively assumes there is a token to use, so you will need to generate your own **classic** GitHub personal access token, which has a rate limit of 5000 per hour. 

To create your own token, follow these steps:
- On GitHub, go to `Profile` -> `Settings` -> `Developer settings`,
- Click the drop-down on `Personal access tokens`,
- Click `Tokens (classic)`,
- Click the drop-down on `Generate new token` and select `Generate new token (classic)`,
- Follow the steps then copy the token into your `.env` file as shown in `.env.example`.
