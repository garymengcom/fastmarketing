from src.constants.enums import SocialMediaEnum
from src.db.models import SocialMedia, get_db


class SocialMediaCrud:
    @staticmethod
    def add(sm: SocialMedia):
        with get_db() as session:
            session.add(sm)
            session.commit()
            session.refresh(sm)

    @staticmethod
    def exist(e: SocialMediaEnum):
        with get_db() as session:
            return session.query(SocialMedia.id).filter(SocialMedia.name == e.name).scalar() is not None