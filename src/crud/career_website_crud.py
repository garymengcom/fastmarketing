from sqlalchemy.dialects.postgresql import insert

from src.constants.enums import WebsiteStatus
from src.db.models import get_db, WordpressWebsite, CareerWebsite
from src.schemas import WordpressWebsiteIn, UrlIn


class CareerWebsiteCrud:
    @staticmethod
    def batch_add(urls: list[UrlIn]):
        data = [u.model_dump() for u in urls if u.url and u.domain]
        if not data:
            return

        with next(get_db()) as db:
            stmt = insert(CareerWebsite).values(data)
            stmt = stmt.on_conflict_do_nothing(index_elements=['domain'])

            db.execute(stmt)
            db.commit()


    @staticmethod
    def get_domains(last_id: int, limit: int = 10) -> list[WordpressWebsite]:
        with next(get_db()) as db:
            return db.query(WordpressWebsite.id, WordpressWebsite.domain)\
                .filter(WordpressWebsite.status == WebsiteStatus.INITIAL.value)\
                .filter(WordpressWebsite.id > last_id)\
                .order_by(WordpressWebsite.id)\
                .limit(limit)\
                .all()

    @staticmethod
    def update_one(d: WordpressWebsiteIn):
        with next(get_db()) as db:
            db.query(CareerWebsite).filter(CareerWebsite.id == d.id).update(d.model_dump(exclude_unset=True))
            db.commit()