from telegram.ext import (ContextTypes, ConversationHandler)
from telegram import Update
from settings import MENU, WEATHER
from db.connection import add_count_to_user
from bot.utils.openweather import get_weather
from bot.utils.magicloop import get_weather_analisis
import logging

logger = logging.getLogger(__name__) 

async def menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Intermediate state that will handle the user's choice and return the next state."""
    logger.info("menu_choice")

    choice = update.message.text
    if choice == '¡Quiero saber el clima!':
        await update.message.reply_text("Has elegido conocer el clima. Por favor, ingresa el nombre de la ciudad:")
        return WEATHER
    
    elif choice == '¡Quiero contar!':
        
        await count_option(update, context)

        return ConversationHandler.END
    
    else:
        await update.message.reply_text("Opción no válida, por favor selecciona una de las opciones del menú.")
        return MENU
    
async def weather_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Weather flow where user asks for a city and the bot will move to the next state with the user input."""
    logger.info("weather_flow")

    city = update.message.text
    weather_response = get_weather(city)
    if weather_response.get('cod', 400) != 200:
        await update.message.reply_text(f"Ha ocurrido un error al obtener el clima de la ciudad {city}, ¿Podrías asegurarte de haber solicitado una ciudad válida?.")
    else:
        analisis = get_weather_analisis(weather_response)
        await update.message.reply_text(analisis)
    return ConversationHandler.END

async def count_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count option to be used in the menu."""
    logger.info("count_option")
    
    user_id = update.effective_user.id    
    actual_user_count = add_count_to_user(user_id)
    if actual_user_count == -1:
        await update.message.reply_text("Ha ocurrido un error al incrementar el contador.")
    else:
        await update.message.reply_text(f"Contador incrementado. Tu contador actual es: {actual_user_count}")