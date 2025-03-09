from telegram import Update
from telegram.ext import (ContextTypes)
from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🤖 *Bienvenido a DeltoBot* 🤖

¡Este bot te ayuda a obtener recomendaciones de ropa basadas en el clima de una ciudad, analizar conversaciones y te ayuda a resumir!

*Comandos disponibles:*
/start - Inicia la conversación con el bot abriendo el menu de opciones.
/resume - Te ayuda a resumir un audio o un PDF.
/help - Muestra este mensaje de ayuda.
/cancel - Cancela la operación actual.
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")