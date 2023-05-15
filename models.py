from sqlalchemy import Column, String, Integer

from database import Base


class BaseUrl(Base):
    __tablename__ = 'baseurl'
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String(255), nullable=False, unique=True)
    short_url = Column(String(255), nullable=False, unique=True)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}





