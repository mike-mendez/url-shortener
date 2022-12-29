from core.config import settings
from crud.base import CRUDBase
from model.models.url_model import URL, URLCreate, URLRead
from secrets import token_urlsafe
from sqlmodel import col, select, Session
from typing import Any, List, Optional

URL_ADDRESS = f"{settings.SERVER_HOST}{settings.API_V1_STR}/url"


class CRUDurl(CRUDBase[URL, URLCreate, URLCreate]):

    def get_urls(self, db: Session) -> List[URL]:
        urls = db.exec(select(self.model).where(self.model.is_active)).all()
        return urls

    def get_url(self, db: Session, url_key: str) -> Optional[URL]:
        results = db.exec(select(self.model).where(col(self.model.key).contains(url_key), self.model.is_active))
        if results:
            forwarded_url = results.one()
            forwarded_url.clicks += 1
            db.add(forwarded_url)
            db.commit()
            db.refresh(forwarded_url)
            return forwarded_url

    def create_url(self, obj_in: URLCreate, db: Session) -> URL:
        # obj_in_data = jsonable_encoder(obj_in)
        # key = obj_in_data.key
        key = obj_in.key
        url_in = self.model(
            key=f"{URL_ADDRESS}/{key}",
            secret_key=f"{URL_ADDRESS}/admin/{key}_{token_urlsafe(8)}",
            # target_url=obj_in_data.target_url,
            target_url=obj_in.target_url,
        )

        db_url = self.model.from_orm(url_in)
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        return db_url


url = CRUDurl(URL)
