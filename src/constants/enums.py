from enum import StrEnum


class DirectoryWebsiteStatus(StrEnum):
    INITIAL = "initial"
    DISABLED = "disabled"
    CREATED = "created"
    NO_SIGNUP = "no_signup"
    CREATED_FAILED = "created_failed"


class WebsiteStatus(StrEnum):
    INITIAL = "initial"
    DISABLED = "disabled"
    SUBMITTED = "submitted"
    SUBMITTED_FAILED = "submitted_failed"