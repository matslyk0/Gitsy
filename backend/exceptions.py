class GitHubAPIError(Exception):
    status_code = 502
    error_message = "GitHub API request failed."


class GitHubTimeOutError(Exception):
    status_code = 504
    error_message = "GitHub did not respond in time."


class InsufficientCommitsError(Exception):
    status_code = 422
    error_message = "Repository has less than 2 Commits."


class InsufficientIssuesError(Exception):
    status_code = 422
    error_message = "Repository has no closed Issues."


class InsufficientPullsError(Exception):
    status_code = 422
    error_message = "Repository has no closed Pull Requests"


class RepoTooLargeError(Exception):
    status_code = 413
    error_message = "Repository must be under 10,000 commits."
