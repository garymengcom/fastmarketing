from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.constants.enums import WebsiteStatus


class WebsiteInfo(BaseModel):
    homepage: str
    title: str = Field(default_factory=str, min_length=60, max_length=120)
    slogan: str = Field(default_factory=str, min_length=60, max_length=80)
    description: str = Field(default_factory=str)
    keywords: str = Field(default_factory=list)
    favicon: str = Field(default_factory=str)
    logo: str = Field(default_factory=str)
    screenshots: str = Field(default_factory=list)


class DirectoryWebsiteOut(BaseModel):
    id: int = Field(default_factory=int)
    domain: str = Field(default_factory=str)

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        populate_by_name = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if isinstance(v, datetime) else v,
        }


class DirectoryWebsiteIn(BaseModel):
    id: int = Field(default_factory=int)
    domain: str = Field(default_factory=str)
    account: str = Field(default_factory=str)
    password: str = Field(default_factory=str)
    status: str = Field(default_factory=str)


class UrlIn(BaseModel):
    url: str = Field(..., description="The URL of the website")
    domain: str = Field(..., description="The domain of the website")


class WordpressWebsiteIn(BaseModel):
    id: int = Field(default_factory=int)
    status: str = Field(default_factory=str)
    failed_reason: str = Field(default_factory=str)


class GoogleSearchRequest(BaseModel):
    q: str = Field(..., description="The query to search for")
    gl: Optional[str] = Field(None, description="The country to search in, e.g. us, uk, ca, au, etc.")
    location: Optional[str] = Field(None, description="The location to search in, e.g. San Francisco, CA, USA")
    hl: Optional[str] = Field(None, description="The language to search in, e.g. en, es, fr, de, etc.")
    tbs: Optional[str] = Field(None, description="The time period to search in, e.g. d, w, m, y")
    num: Optional[int] = Field(10, ge=1, le=100, description="The number of results to return, max is 100")
    page: Optional[int] = Field(1, ge=1, le=100, description="The page number to return, max is 100")
