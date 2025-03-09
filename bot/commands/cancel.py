from telegram import Update
from telegram.ext import (ContextTypes)

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Command to cancel the current flow and end the conversation."""

    await update.message.reply_text(
        'Cancelando la operación actual.\nMuchas gracias por usar el DeltoBot.',
    )

    return ConversationHandler.END