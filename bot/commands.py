from telegram import (ReplyKeyboardMarkup, Update)
from telegram.ext import (ContextTypes, ConversationHandler)
from settings import MENU, WEATHER, COUNT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['¡Quiero saber el clima!', '¡Quiero contar!']]
    await update.message.reply_text(
        '<b>¡Bienvenido al DeltoBot!</b>\n'
        '¿En qué te puedo ayudar hoy?',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return MENU

async def menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    # Aquí obtendrías el nombre de la ciudad
    city = update.message.text
    # Lógica para llamar a la API del clima e interpretar la respuesta
    await update.message.reply_text(f"Mostrando el clima para {city} (esta funcionalidad se implementará)...")
    return ConversationHandler.END

async def count_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Aquí se implementaría la lógica del contador (por ejemplo, incrementar y persistir)
    await update.message.reply_text("Contador incrementado. (Esta funcionalidad se implementará)...")
    return ConversationHandler.END