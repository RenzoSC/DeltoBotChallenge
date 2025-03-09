from telegram import Update
from telegram.ext import (ContextTypes)
from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help message to show the user the available commands."""
    help_text = """
🤖 *Bienvenido a DeltoBot* 🤖

¡Este bot puede ayudarte a ver el clima de una ciudad, obtener recomendaciones de ropa basada en el clima, analizar conversaciones y resumir audios o PDFs!

*Comandos disponibles:*
/start - Inicia la conversación con el bot abriendo el menu de opciones.
/resume - Te ayuda a resumir un audio o un PDF.
/help - Muestra este mensaje de ayuda.
/cancel - Cancela la operación actual.
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")