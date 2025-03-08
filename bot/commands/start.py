from telegram import (ReplyKeyboardMarkup, Update)
from telegram.ext import (ContextTypes)
from settings import MENU
from db.connection import add_user_if_not_exists

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Principal menu where user can choose between weather and count. It will return the next state."""
    
    user_id = update.effective_user.id
    
    add_user_if_not_exists(user_id)

    reply_keyboard = [['¡Quiero saber el clima!', '¡Quiero contar!', '¡Quiero analizar nuestra conversación!']]
    
    await update.message.reply_text(
        '<b>¡Bienvenido al DeltoBot!</b>\n'
        '¿En qué te puedo ayudar hoy?',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return MENU