from sqlalchemy.dialects.postgresql import insert

from src.constants.enums import WebsiteStatus
from src.db.models import get_db, WordpressWebsite
from src.schemas import WordpressWebsiteIn


class WordpressWebsiteCrud:
    @staticmethod
    def batch_add_domains(domains: list[str]):
        with next(get_db()) as db:
            data = [{"domain": d.lower()} for d in set(domains) if d]
            if not data:
                return

            stmt = insert(WordpressWebsite).values(data)
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
    def update_domain(d: WordpressWebsiteIn):
        with next(get_db()) as db:
            db.query(WordpressWebsite).filter(WordpressWebsite.id == d.id).update(d.model_dump(exclude_unset=True))
            db.commit()