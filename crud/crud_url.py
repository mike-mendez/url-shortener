from fastapi.encoders import jsonable_encoder
from model.models.url_model import URL, URLBase, URLCreate, URLRead
from pydantic import BaseModel
from sqlmodel import Session
from typing import List


class CRUDurl(BaseModel):
    def get_all(self):
        pass

    def get_one_by_secret_key(self):
        pass

    def

    # def get_all(self):
    #     pass
    # def get_by_secret_key(self):
    #     pass
    # def create(
    #         self, db: Session, *, obj_in: URLCreate, owner_id: int
    # ) -> URLBase:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, owner_id=owner_id)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj
    #
    # def get_multi(
    #         self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    # ) -> List[URLBase]:
    #     return (
    #         db.query(self.model)
    #         .filter( == owner_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )


url = CRUDurl()


