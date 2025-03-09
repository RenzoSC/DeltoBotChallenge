from telegram.ext import (ContextTypes, ConversationHandler)
from telegram import Update, File, ReplyKeyboardMarkup, InputFile
from settings import RESUME_OPTIONS_MENU, RESUME_AUDIO, RESUME_PDF, RESUME_FORMAT
from bot.services.openai import summarize_audio, summarize_pdf, convert_text_to_audio
import logging

logger = logging.getLogger(__name__) 

async def resume_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Intermediate state that will handle the user's choice and return the next state."""
    logger.info("menu_choice")

    choice = update.message.text
    
    if choice == 'Audio':
        await update.message.reply_text("Has elegido resumir un audio. Por favor, ingresa el audio que deseas resumir a continuación:")

        return RESUME_AUDIO
    
    elif choice == 'PDF':
        await update.message.reply_text("Has elegido resumir un PDF. Por favor, ingresa el archivo PDF que deseas resumir a continuación:")
        
        return RESUME_PDF

    else:
        reply_keyboard = [['PDF', 'Audio']]
        await update.message.reply_text("Opción no válida, por favor elige entre 'PDF' o 'Audio'.",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        
        return RESUME_OPTIONS_MENU
    
async def resume_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Resume audio flow where user sends an audio and the bot will reply with the summary."""
    logger.info("resume_audio")
    extension = ""
    if update.message.voice:
        audio_file:File = await update.message.voice.get_file()
        extension = ".ogg"
    elif update.message.audio:
        audio_file:File = await update.message.audio.get_file()
        extension = ".m4a"
    else:
        await update.message.reply_text("No se ha enviado un archivo de audio válido.")
        return ConversationHandler.END
    
    await update.message.reply_text("Procesando audio...")

    audio_response = await summarize_audio(audio_file, extension)
    context.user_data['summary'] = audio_response
    
    await update.message.reply_text("Resumen generado. ¿Te gustaría recibirlo en formato de texto o audio?", 
                                    reply_markup=ReplyKeyboardMarkup([['Texto', 'Audio']], one_time_keyboard=True, resize_keyboard=True))
    
    return RESUME_FORMAT

async def resume_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Resume pdf flow where user sends a PDF file and the bot will reply with the summary"""
    logger.info("resume_pdf")
    
    document = update.message.document
    file_name = document.file_name

    if not file_name.lower().endswith('.pdf'):
        await update.message.reply_text("El archivo que enviaste no es un PDF. Por favor, envía un archivo con extensión .pdf")
        return ConversationHandler.END
    
    pdf_file:File = await document.get_file()

    await update.message.reply_text("Procesando PDF...")

    resume_pdf_response = await summarize_pdf(pdf_file)

    context.user_data['summary'] = resume_pdf_response

    await update.message.reply_text("Resumen generado. ¿Te gustaría recibirlo en formato de texto o audio?", 
                                    reply_markup=ReplyKeyboardMarkup([['Texto', 'Audio']], one_time_keyboard=True, resize_keyboard=True))

    return RESUME_FORMAT

async def resume_format_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle user's choice of receiving the summary in text or audio format."""
    logger.info("resume_format_choice")
    
    choice = update.message.text
    summary_text = context.user_data.get('summary', 'Algo salió mal al generar el resumen.')
    
    if choice == 'Texto':
        await update.message.reply_text(summary_text)
    
    elif choice == 'Audio':
        
        with convert_text_to_audio(summary_text) as audio:
            await update.message.reply_voice(
                voice=InputFile(audio, filename="resumen.mp3"),
                caption="Resumen en audio 🎧"
            )

    else:
        reply_keyboard = [['Texto', 'Audio']]
        await update.message.reply_text("Opción no válida. Por favor, elige entre 'Texto' o 'Audio'.",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        
        return RESUME_FORMAT
    
    return ConversationHandler.END