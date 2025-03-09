from db.main import SessionLocal
from db.tables import TelegramUser, TelegramClothGenerationUses
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from settings import MAX_CLOTH_GENERATION_USES
import logging

logger = logging.getLogger(__name__) 

def add_user_if_not_exists(user_id: int):
    """Adds a user to the database if it does not exist.

    Args:
    - user_id: id of the user to be added
    """
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
    """Deletes a user from the database.
    
    Args:
    - user_id: id of the user to be deleted
    """
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
    if user does not exist, it will be created with count = 1.
    If an error occurs, returns -1 -> this is the error flag for this function.

    Args:
    - user_id: id of the user to be updated
    """
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

def add_user_cloth_generation_if_not_exists(user_id: int):
    """Adds a user to the cloth generation uses table if it does not exist.
    
    Args:
    - user_id: id of the user to be added
    """
    
    db:Session = SessionLocal()
    try:
        user = db.query(TelegramClothGenerationUses).filter(TelegramClothGenerationUses.id == user_id).first()
        if not user:
            new_user = TelegramClothGenerationUses(id=user_id)
            db.add(new_user)
            db.commit()
            logger.info(f"User {user_id} added to the database.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

def reset_user_count_if_new_day(user:TelegramClothGenerationUses, db:Session):
    """Resets the count of the user if the date of the last count is different from today
    
    Args:
    - user: user to be checked (TelegramClothGenerationUses)
    - db: database session
    """

    today = datetime.now().date()
    user_date = user.count_date
    if user_date<today:
        user.count = 0
        user.count_date = today
        db.commit()
        logger.info(f"User {user.id} count reseted.")

def reached_cloth_generation_limit(user_id:int)->int:
    """Check if the user has reached the limit of cloth generation uses. Resets the count if the date of the last count is different from today.
    
    Args:
    - user_id: id of the user to be checked

    Returns:
    - 1 if the user has reached the limit
    - 0 if the user has not reached the limit
    - -1 if an error occurs
    """
    
    db:Session = SessionLocal()
    try:
        user = db.query(TelegramClothGenerationUses).filter(TelegramClothGenerationUses.id == user_id).first()

        if user:
            reset_user_count_if_new_day(user, db=db)
            db.refresh(user)

            if user.count >= MAX_CLOTH_GENERATION_USES:
                logger.info(f"User {user_id} reached the limit of cloth generation uses.")
                return 1
            else:
                return 0
        else:
            logger.error(f"User {user_id} not found in the database.")
            return -1
    except Exception as e:
        logger.error(f"An error occurred on reached_cloth_generation_limit: {e}")
        return -1
    finally:
        db.close()

def add_count_cloth_generation(user_id:int)->int:
    """Adds 1 to the count of cloth generation uses of the user with the given id.

    Args:
    - user_id: id of the user to be updated

    Returns:
    - actual user count if the operation is successful
    - -1 if an error occurs
    """ 
    
    db:Session = SessionLocal()
    try:
        user = db.query(TelegramClothGenerationUses).filter(TelegramClothGenerationUses.id == user_id).first()
        if user:
            actual_count = user.count
            user.count += 1
            db.commit()
            logger.info(f"User {user_id} count updated.")
            return actual_count+1
        
    except Exception as e:
        logger.error(f"An error occurred on add_count_cloth_generation: {e}")
        db.rollback()
        return -1
    finally:
        db.close()