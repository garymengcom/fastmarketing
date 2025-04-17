from dataclasses import dataclass
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

from src.utils.env_utils import check_env_vars, get_list

ROOT_DIR = Path(__file__).parent.parent


@dataclass
class BasicConfig:
    gmail_account: str = getenv("GMAIL_ACCOUNT")
    gmail_password: str = getenv("GMAIL_PASSWORD")
    mobile_number: str = getenv("MOBILE_NUMBER")
    website_homepage: str = getenv("WEBSITE_HOMEPAGE")
    social_media_usernames: str = get_list("SOCIAL_MEDIA_USERNAME")


@dataclass
class DirConfig:
    build_dir: Path = Path(getenv("BUILD_DIR", ROOT_DIR / "build"))
    accounts_dir: Path = Path(getenv("ACCOUNTS_DIR", ROOT_DIR / "accounts"))


@dataclass
class LlmConfig:
    base_url: str = getenv("LLM_ENDPOINT")
    api_key: str = getenv("LLM_API_KEY")


load_dotenv()
check_env_vars(BasicConfig, LlmConfig)

DirConfig.accounts_dir.mkdir(parents=True, exist_ok=True)
