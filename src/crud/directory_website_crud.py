from sqlalchemy.dialects.postgresql import insert

from src.constants.enums import DirectoryWebsiteStatus
from src.db.models import get_db, DirectoryWebsite
from src.schemas import WordpressWebsiteIn


class DirectoryWebsiteCrud:
    @staticmethod
    def batch_add_domains(domains: list[str]):
        with next(get_db()) as db:
            data = [{"domain": d.lower()} for d in set(domains) if d]
            if not data:
                return

            stmt = insert(DirectoryWebsite).values(data)
            stmt = stmt.on_conflict_do_nothing(index_elements=['domain'])

            db.execute(stmt)
            db.commit()


    @staticmethod
    def get_domains() -> list[DirectoryWebsite]:
        with next(get_db()) as db:
            return db.query(DirectoryWebsite.id, DirectoryWebsite.domain)\
                .filter(DirectoryWebsite.status == DirectoryWebsiteStatus.INITIAL.value)\
                .all()

    @staticmethod
    def update_domain(d: WordpressWebsiteIn):
        with next(get_db()) as db:
            db.query(DirectoryWebsite).filter(DirectoryWebsite.id == d.id).update(d.model_dump())
            db.commit()