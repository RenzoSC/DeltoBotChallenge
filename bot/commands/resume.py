from telegram import (ReplyKeyboardMarkup, Update)
from telegram.ext import (ContextTypes)
from settings import RESUME_OPTIONS_MENU

async def resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Principal menu where user can choose between weather and count. It will return the next state."""

    reply_keyboard = [['PDF', 'Audio']]
    
    await update.message.reply_text(
        '¿Qué te gustaría resumir ahora?',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return RESUME_OPTIONS_MENU