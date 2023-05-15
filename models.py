from sqlalchemy import Column, String, Integer

from database import Base


class BaseUrl(Base):
    __tablename__ = 'baseurl'
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String)
    short_url = Column(String)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}





