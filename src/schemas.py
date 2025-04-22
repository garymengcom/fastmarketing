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

