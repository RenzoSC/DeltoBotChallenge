import pytest
from unittest.mock import MagicMock
from db.connection import add_user_if_not_exists
from db.tables import TelegramUser
from sqlalchemy.orm import Session
from unittest.mock import patch

@pytest.mark.asyncio
async def test_add_user_if_not_exists():
    #mock for dbsession
    mock_db = MagicMock()

    #patch sessionlocal with mock
    with patch('db.connection.SessionLocal', return_value=mock_db):
        #simulates db query returning None
        mock_db.query.return_value.filter.return_value.first.return_value = None

        #call the function with a user_id
        user_id = 123456
        add_user_if_not_exists(user_id)

        #verifications
        mock_db.query.return_value.filter.return_value.first.assert_called_once()

        mock_db.add.assert_called_once()

        mock_db.commit.assert_called_once()

        mock_db.close.assert_called_once()


@pytest.mark.asyncio
async def test_user_exists():
    #mock for dbsession
    mock_db = MagicMock(Session)

    #patch sessionlocal with mock
    with patch('db.connection.SessionLocal', return_value=mock_db):
        #simulates db query returning a user
        mock_db.query.return_value.filter.return_value.first.return_value = TelegramUser(id=123456)
        
        #call the function with a user_id
        user_id = 123456
        add_user_if_not_exists(user_id)

        #verifications
        mock_db.add.assert_not_called()
        mock_db.commit.assert_not_called()
        mock_db.rollback.assert_not_called()
        mock_db.close.assert_called_once()