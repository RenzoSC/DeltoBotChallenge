from db.main import SessionLocal
from db.tables import TelegramUser
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__) 

def add_user_if_not_exists(user_id: int):
    db:Session = SessionLocal()
    try:
        user = db.query(TelegramUser).filter(TelegramUser.id == user_id).first()
        if not user:
            new_user = TelegramUser(id=user_id)
            db.add(new_user)
            db.commit()
            logger.info(f"User {user_id} added to the database.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

def delete_user(user_id: int):
    db:Session = SessionLocal()
    try:
        user = db.query(TelegramUser).filter(TelegramUser.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            logger.info(f"User {user_id} deleted from the database.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()