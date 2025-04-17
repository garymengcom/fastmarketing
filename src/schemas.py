from pydantic import BaseModel, Field


class BasicInfo(BaseModel):
    gmail: str
    gmail_password: str
    mobile: str


class WebsiteInfo(BaseModel):
    homepage: str
    title: str = Field(default_factory=str, min_length=60, max_length=120)
    slogan: str = Field(default_factory=str, min_length=60, max_length=80)
    description: str = Field(default_factory=str)
    keywords: str = Field(default_factory=list)


class ImageInfo(BaseModel):
    favicon: str = Field(default_factory=str)
    logo: str = Field(default_factory=str)
    screenshots: str = Field(default_factory=list)


class SocialMediaAccountInfo(BaseModel):
    facebook: str = Field(default_factory=str)
    facebook_password: str = Field(default_factory=str)
    twitter: str = Field(default_factory=str)
    twitter_password: str = Field(default_factory=str)
    linkedin: str = Field(default_factory=str)
    linkedin_password: str = Field(default_factory=str)
    instagram: str = Field(default_factory=str)
    instagram_password: str = Field(default_factory=str)
    github: str = Field(default_factory=str)
    github_password: str = Field(default_factory=str)


class VideoPlatformAccountInfo(BaseModel):
    youtube: str = Field(default_factory=str)
    youtube_password: str = Field(default_factory=str)
    vimeo: str = Field(default_factory=str)
    vimeo_password: str = Field(default_factory=str)
    dailymotion: str = Field(default_factory=str)
    dailymotion_password: str = Field(default_factory=str)
    tiktok: str = Field(default_factory=str)
    tiktok_password: str = Field(default_factory=str)
    twitch: str = Field(default_factory=str)
    twitch_password: str = Field(default_factory=str)