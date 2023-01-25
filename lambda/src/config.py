import os


class Config:
    github_token: str

    def __init__(self):

        # GitHub token. Must have 'repo' scope.
        self.github_token = os.getenv("GITHUB_TOKEN")
