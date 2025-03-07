import pytest
from types import SimpleNamespace
from bot.flows.start_flow import menu_choice
from settings import MENU, WEATHER, COUNT
from tests.helpers import MyUpdater

@pytest.mark.asyncio
async def test_menu_choice_weather():
    #simulates the user choosing the weather option
    dummy_update = MyUpdater("¡Quiero saber el clima!")
    dummy_context = SimpleNamespace()
    state = await menu_choice(dummy_update, dummy_context)

    #verifications
    assert state == WEATHER
    assert dummy_update.message.replies, "No se envió respuesta en menu_choice para clima"
    assert "Has elegido conocer el clima" in dummy_update.message.replies[0]

@pytest.mark.asyncio
async def test_menu_choice_count():
    #simulates the user choosing the count option
    dummy_update = MyUpdater("¡Quiero contar!")
    dummy_context = SimpleNamespace()
    state = await menu_choice(dummy_update, dummy_context)
    
    #verifications
    assert state == COUNT
    assert dummy_update.message.replies, "No se envió respuesta en menu_choice para contar"
    assert "Has elegido contar" in dummy_update.message.replies[0]

@pytest.mark.asyncio
async def test_menu_choice_invalid():
    #simulates user choosing an invalid option
    dummy_update = MyUpdater("Opción inválida")
    dummy_context = SimpleNamespace()
    state = await menu_choice(dummy_update, dummy_context)
    
    #verifications
    assert state == MENU
    assert dummy_update.message.replies, "No se envió respuesta en menu_choice para opción inválida"
    assert "Opción no válida" in dummy_update.message.replies[0]