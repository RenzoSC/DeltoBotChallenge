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