from dataclasses import dataclass
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

from src.utils.env_utils import check_env_vars, get_list

ROOT_DIR = Path(__file__).parent.parent.parent


@dataclass
class BasicConfig:
    gmail_account: str = getenv("GMAIL_ACCOUNT")
    gmail_password: str = getenv("GMAIL_PASSWORD")
    mobile_number: str = getenv("MOBILE_NUMBER")
    website_title: str = getenv("WEBSITE_TITLE")
    website_description: str = getenv("WEBSITE_DESCRIPTION")
    website_homepage: str = getenv("WEBSITE_HOMEPAGE")
    date_of_birth: str = getenv("DATE_OF_BIRTH")
    gender: str = getenv("GENDER", "male")
    social_media_usernames: str = get_list("SOCIAL_MEDIA_USERNAME")
    signup_password: str = get_list("SIGNUP_PASSWORD")


@dataclass
class DbConfig:
    URL: str = getenv("DB_URL")

@dataclass
class DirConfig:
    build_dir: Path = Path(getenv("BUILD_DIR", ROOT_DIR / "build"))
    basic_info_dir: Path = Path(getenv("BASIC_INFO_DIR", ROOT_DIR / "build/basic_info"))
    cookies_dir: Path = Path(getenv("COOKIES_DIR", ROOT_DIR / "build/cookies"))
    logs_dir: Path = Path(getenv("LOGS_DIR", ROOT_DIR / "build/logs"))


@dataclass
class ApiKeyConfig:
    llm_base_url: str = getenv("LLM_ENDPOINT")
    llm_api_key: str = getenv("LLM_API_KEY")
    serper_api_key: str = getenv("SERPER_API_KEY")


load_dotenv()
check_env_vars(BasicConfig, ApiKeyConfig, DbConfig)

DirConfig.basic_info_dir.mkdir(parents=True, exist_ok=True)
