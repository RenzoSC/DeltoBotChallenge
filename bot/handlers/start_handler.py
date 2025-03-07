from telegram.ext import (CommandHandler, ConversationHandler, MessageHandler, filters)
from settings import MENU, WEATHER
from bot.commands.start import start
from bot.flows.start_flow import menu_choice, weather_flow

def get_start_handler():
    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_choice)],
            WEATHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, weather_flow)],
        },
        fallbacks=[CommandHandler('cancel', start)]
    )
    return start_handler