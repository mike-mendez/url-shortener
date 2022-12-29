from core.config import settings
from secrets import token_urlsafe
from sqlmodel import Field, SQLModel
from typing import Optional


class URLBase(SQLModel):
    target_url: str = Field(nullable=False)
    key: str = Field(default=f"{settings.SERVER_HOST}{settings.API_V1_STR}/url/{token_urlsafe(5)}",
                     nullable=False,
                     unique=True,
                     index=True)


class URL(URLBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    secret_key: Optional[str] = Field(unique=True, index=True)
    is_active: Optional[bool] = Field(default=True)
    clicks: Optional[int] = Field(default=0)


class URLCreate(URLBase):
    pass

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "key": "abc123",
                "target_url": "https://www.google.com/search?q=url+shortener&source=hp&ei=6AWsY5K-Harf2roPrcit-AI&iflsig=AJiK0e8AAAAAY6wT-C2zHymb3EWrjYDqZh8AxUIqMzws&oq=URL+s&gs_lcp=Cgdnd3Mtd2l6EAMYADIECAAQQzIFCAAQkQIyBAgAEEMyBAgAEEMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6FAgAEOoCELQCEIoDELcDENQDEOUCOgoILhDHARDRAxBDOgsILhCABBDHARDRA0oFCEASATFQnlxY8WFgjXBoAXAAeACAAXuIAbIEkgEDMC41mAEAoAEBsAEK&sclient=gws-wiz"
            }
        }


class URLRead(URLBase):
    id: int
    key: str
    secret_key: str
    is_active: bool
    clicks: int
