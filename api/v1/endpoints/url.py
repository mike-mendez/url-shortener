from core.config import settings
from crud import crud_url
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from model.database.database import get_session
from model.models.url_model import URL, URLCreate, URLRead
from requests import get
from requests.exceptions import ConnectionError
from sqlalchemy.exc import IntegrityError
from sqlmodel import col, select, Session
from typing import Any, List
import validators


URL_ADDRESS = f"{settings.SERVER_HOST}{settings.API_V1_STR}/url"
router = APIRouter()


@router.get("/", response_model=List[URLRead])
def get_urls(db: Session = Depends(get_session)) -> Any:
    # tests = crud_url.get_multi(db)
    urls = crud_url.url.get_urls(db)
    # urls = db.exec(select(URL).where(URL.is_active)).all()
    return urls


@router.post("/", response_model=URLRead)
async def create_url(url_in: URLCreate, db: Session = Depends(get_session)) -> Any:
    if not validators.url(url_in.target_url):
        raise HTTPException(status_code=400,
                            detail="Provided URL was not valid.")
    url = crud_url.url.create_url(url_in, db)
    # key = url_in.key
    # url = URL(
    #     key=f"{URL_ADDRESS}/{key}",
    #     secret_key=f"{URL_ADDRESS}/admin/{key}_{token_urlsafe(8)}",
    #     target_url=url_in.target_url,
    # )
    #
    # db_url = URL.from_orm(url)
    # db.add(db_url)
    # db.commit()
    # db.refresh(db_url)
    # return db_url
    return url


@router.get("/{url_key}")
async def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_session)) -> Any:
    # results = db.exec(select(URL).where(col(URLRead.key).contains(url_key), URL.is_active))
    url = crud_url.url.get_url(db, url_key)
    # if results:
    #     url = results.one()
    #     url.clicks += 1
    #     db.add(url)
    #     db.commit()
    #     db.refresh(url)
    try:
        url_check = get(url.target_url)
    except ConnectionError:
        raise HTTPException(status_code=404,
                            detail=f"URL '{request.url}' does not exist")
    else:
        return RedirectResponse(url.target_url)


@router.get("/admin/{secret_key}", response_model=URLRead)
async def get_url_by_secret_key(secret_key: str, db: Session = Depends(get_session)) -> Any:
    results = db.exec(select(URL).where(col(URLRead.secret_key).contains(secret_key), URL.is_active))
    if results:
        url_info = results.one()
        return url_info
    raise HTTPException(status_code=404,
                        detail=f"Secret Key '{secret_key} does not exist")


@router.patch("/admin/{secret_key}", name="deactivating_shortened_url")
async def delete_url(secret_key: str, db: Session = Depends(get_session)) -> Any:
    results = db.exec(select(URL).where(col(URLRead.secret_key).contains(secret_key)))
    if results:
        url = results.one()
        url.is_active = False
        db.add(url)
        db.commit()
        db.refresh(url)
        return {"message": f"Shortened URL for '{url.target_url}' has been deactivated."}
    raise HTTPException(status_code=404,
                        detail=f"Secret Key '{secret_key} does not exist")


@router.get("/peek/{shortened_url}")
async def peek_url(shortened_url: str, db: Session = Depends(get_session)) -> Any:
    results = db.exec(select(URL).where(URLRead.key == shortened_url))
    if results:
        target_url = results.one().target_url
        return {"message": f"'{shortened_url}' is the shortened url for '{target_url}'."}
    raise HTTPException(status_code=404,
                        detail=f"Shortened URL '{shortened_url} does not exist")
