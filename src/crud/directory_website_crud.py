from sqlalchemy.dialects.postgresql import insert

from src.db.models import get_db, DirectoryWebsite


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
