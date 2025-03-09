from telegram.ext import (CommandHandler, ConversationHandler, MessageHandler, filters)
from settings import RESUME_OPTIONS_MENU, RESUME_AUDIO, RESUME_PDF, RESUME_FORMAT
from bot.commands.resume import resume_command
from bot.flows.resume_flow import resume_menu_choice, resume_audio, resume_pdf, resume_format_choice

def get_resume_handler():
    start_handler = ConversationHandler(
        entry_points=[CommandHandler('resume', resume_command)],
        states={
            RESUME_OPTIONS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, resume_menu_choice)],
            RESUME_AUDIO: [MessageHandler(filters.VOICE & ~filters.COMMAND, resume_audio), MessageHandler(filters.AUDIO & ~filters.COMMAND, resume_audio)],
            RESUME_PDF: [MessageHandler(filters.Document.PDF & ~filters.COMMAND, resume_pdf)],
            RESUME_FORMAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, resume_format_choice)]
        },
        fallbacks=[CommandHandler('cancel', resume_command)]
    )
    return start_handler