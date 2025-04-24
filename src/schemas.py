from datetime import datetime

from pydantic import BaseModel, Field


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
        orm_mode = True
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
