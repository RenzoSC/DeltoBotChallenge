# tests/test_bot.py
import pytest
from types import SimpleNamespace
from bot.commands.start import start
from bot.flows.start_flow import menu_choice
from settings import MENU, WEATHER, COUNT
from tests.helpers import MyUpdater

@pytest.mark.asyncio
async def test_start():
    #Simulates the initial conversation between the user and the bot
    dummy_update = MyUpdater("/start")
    dummy_context = SimpleNamespace()
    state = await start(dummy_update, dummy_context)
    
    # Verifies that the state returned is MENU
    assert state == MENU

    # Verifies that the replies are not empty and that the message sendend is the welcome message
    assert dummy_update.message.replies, "No se envió respuesta en /start"
    assert "¡Bienvenido al DeltoBot!" in dummy_update.message.replies[0]

@pytest.mark.asyncio
async def test_menu_choice_weather():
    #Simulates the user choosing the weather option
    dummy_update = MyUpdater("¡Quiero saber el clima!")
    dummy_context = SimpleNamespace()
    state = await menu_choice(dummy_update, dummy_context)

    #Verifies the state returned is WEATHER
    assert state == WEATHER
    
    # Verifies that the replies are not empty and that the message sendend is correct
    assert dummy_update.message.replies, "No se envió respuesta en menu_choice para clima"
    assert "Has elegido conocer el clima" in dummy_update.message.replies[0]

@pytest.mark.asyncio
async def test_menu_choice_count():
    #Simulates the user choosing the count option
    dummy_update = MyUpdater("¡Quiero contar!")
    dummy_context = SimpleNamespace()
    state = await menu_choice(dummy_update, dummy_context)
    
    #Verifies the state returned is COUNT
    assert state == COUNT

    # Verifies that the replies are not empty and that the message sendend is correct
    assert dummy_update.message.replies, "No se envió respuesta en menu_choice para contar"
    assert "Has elegido contar" in dummy_update.message.replies[0]

@pytest.mark.asyncio
async def test_menu_choice_invalid():
    #simulates user choosing an invalid option
    dummy_update = MyUpdater("Opción inválida")
    dummy_context = SimpleNamespace()
    state = await menu_choice(dummy_update, dummy_context)
    
    # Verifies the state returned is MENU
    assert state == MENU
    
    # Verifies that the replies are not empty and that the message sendend is correct
    assert dummy_update.message.replies, "No se envió respuesta en menu_choice para opción inválida"
    assert "Opción no válida" in dummy_update.message.replies[0]
