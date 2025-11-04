class GitHubAPIError(Exception):
    pass


class GitHubTimeOutError(Exception):
    pass


class InsufficientDataError(Exception):
    pass


class TimeOutOfBoundsError(Exception):
    pass


class RepoTooLargeError(Exception):
    pass
