"""
A `tracker.values` model that contains all hardcoded values for tracking purposes
"""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

REQUEST_TIMEOUT: int = 10  # in seconds
ISSUES_URL: str = "https://api.github.com/repos/{owner}/{repo}/issues"
PULLS_URL: str = "https://api.github.com/repos/{owner}/{repo}/pulls"
PULLS_REVIEWS_URL: str = (
    "https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews"
)

ROLE_MAX_CHARACTER_LENGTH: int = 11
ISSUES_SEARCH: str = (
    "https://api.github.com/search/issues?q=assignee:{username}+is:issue"
)

HEADERS: dict = {
    "Accept": "application/vnd.github+json",
    "Authorization": f'Bearer {os.environ.get("GITHUB_AUTH_TOKEN", "")}',
    "X-GitHub-Api-Version": "2022-11-28",
}

DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
SECONDS_IN_AN_HOUR: int = 3600


@dataclass(frozen=True)
class DefaultModelValues:
    """
    A data class to store default maximum length values for various fields in models.

    Attributes:
    - name_max_length (int): The maximum allowed length for the 'name' field. Default is 255.
    - author_max_length (int): The maximum allowed length for the 'author' field. Default is 255.
    - link_max_length (int): The maximum allowed length for the 'link' field. Default is 255.
    - email_max_length (int): The maximum allowed length for the 'email' field. Default is 255.
    - title_max_length (int): The maximum allowed length for the 'title' field. Default is 255.

    This class is immutable, so its values cannot be modified after instantiation.
    """

    name_max_length: int = 255
    author_max_length: int = 255
    link_max_length: int = 255
    email_max_length: int = 255
    time_limit_default: int = 86400
