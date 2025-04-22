from datetime import datetime

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, DateTime
from sqlalchemy import Column, Integer, String

from src.constants.config import DbConfig

engine = create_engine(DbConfig.URL, pool_pre_ping=True)
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


class SocialMedia(Base):
    __tablename__ = "social_medias"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    domain = Column(String(50))
    account = Column(String(50))
    email = Column(String(50))
    password = Column(String(128))


class DirectoryWebsite(Base):
    __tablename__ = "directory_websites"

    id = Column(Integer, primary_key=True)
    domain = Column(String(50), nullable=False, unique=True)
    account = Column(String(50), nullable=False, default="")
    password = Column(String(128), nullable=False, default="")
    status = Column(String(20), nullable=False, default="enabled")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


if __name__ == '__main__':
    Base.metadata.create_all(engine)

