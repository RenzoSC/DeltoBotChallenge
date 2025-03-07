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

def add_count_to_user(user_id: int) -> int:
    """Adds 1 to the count of the user with the given id, 
    if user does not exist, it will be created with count = 1
    
    returns actual user count
    if an error occurs, returns -1 -> this is the error flag for this function"""
    
    db:Session = SessionLocal()
    try:

        user = db.query(TelegramUser).filter(TelegramUser.id == user_id).first()
        if user:
            actual_count = user.count
            user.count += 1
            db.commit()
            logger.info(f"User {user_id} count updated.")
            return actual_count+1
        else:
            new_user = TelegramUser(id=user_id, count=1)
            db.add(new_user)
            db.commit()
            logger.info(f"User {user_id} added to the database with count = 1.")
            return 1
    except Exception as e:
        logger.error(f"An error occurred on add_count_to_user: {e}")
        db.rollback()
        return -1
    finally:
        db.close()