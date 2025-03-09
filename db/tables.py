from sqlalchemy import Column, BigInteger, Integer, Date, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TelegramUser(Base):
    __tablename__ = "telegram_users"
    id = Column(BigInteger, primary_key=True, index=True)
    count = Column(Integer, default=0, nullable=False)


class TelegramClothGenerationUses(Base):
    __tablename__ = "telegram_cloth_generation_uses"
    id = Column(BigInteger, primary_key=True, index=True)
    count = Column(Integer, default=0, nullable=False)
    count_date = Column(Date, server_default=func.current_date(), nullable=False)