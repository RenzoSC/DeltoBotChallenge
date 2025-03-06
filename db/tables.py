from sqlalchemy import Column, BigInteger, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TelegramUser(Base):
    __tablename__ = "telegram_users"
    id = Column(BigInteger, primary_key=True, index=True)
    count = Column(Integer, default=0, nullable=False)