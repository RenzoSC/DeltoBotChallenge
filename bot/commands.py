from telegram import (ReplyKeyboardMarkup, Update)
from telegram.ext import (ContextTypes, ConversationHandler)
from settings import MENU, WEATHER, COUNT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Principal menu where user can choose between weather and count. It will return the next state."""
    
    reply_keyboard = [['¡Quiero saber el clima!', '¡Quiero contar!']]
    
    await update.message.reply_text(
        '<b>¡Bienvenido al DeltoBot!</b>\n'
        '¿En qué te puedo ayudar hoy?',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return MENU

async def menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Intermediate state that will handle the user's choice and return the next state."""

    choice = update.message.text
    if choice == '¡Quiero saber el clima!':
        await update.message.reply_text("Has elegido conocer el clima. Por favor, ingresa el nombre de la ciudad:")
        return WEATHER
    elif choice == '¡Quiero contar!':
        await update.message.reply_text("Has elegido contar. Se incrementará tu contador. ¡Espera un momento...")
        return COUNT
    else:
        await update.message.reply_text("Opción no válida, por favor selecciona una de las opciones del menú.")
        return MENU
    
async def weather_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Weather flow where user asks for a city and the bot will move to the next state with the user input."""
    
    city = update.message.text
    
    await update.message.reply_text(f"Mostrando el clima para {city} (esta funcionalidad se implementará)...")
    return ConversationHandler.END

async def count_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Count flow where the User will add 1 to his own counter."""
    
    await update.message.reply_text("Contador incrementado. (Esta funcionalidad se implementará)...")
    return ConversationHandler.END