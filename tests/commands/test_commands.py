import pytest
from types import SimpleNamespace
from unittest.mock import patch
from bot.commands.start import start
from settings import MENU
from tests.helpers import MyUpdater

@pytest.mark.asyncio
async def test_start():
    #patch add_user_if_not_exists to avoid interaction with the DB
    with patch('bot.commands.start.add_user_if_not_exists') as mock_add_user:
        
        #avoiding the interaction with the DB
        mock_add_user.db.return_value.query.return_value.filter.return_value.first.return_value = None
        
        #simulates the user sending the /start command
        dummy_update = MyUpdater("/start")
        dummy_context = SimpleNamespace()

        #call the start command
        state = await start(dummy_update, dummy_context)

        #verifications
        mock_add_user.assert_called_once_with(dummy_update.effective_user.id)
        assert state == MENU
        assert dummy_update.message.replies, "No se envió respuesta en /start"
        assert "¡Bienvenido al DeltoBot!" in dummy_update.message.replies[0]


