from telegram.ext import (CommandHandler, ConversationHandler, MessageHandler, filters)
from settings import MENU, WEATHER, ANALIZE_CONVERSATION, CLOTH_RECOMENDATIONS
from bot.commands.start import start
from bot.commands.cancel import cancel_command
from bot.commands.help import help_command
from bot.flows.start_flow import menu_choice, weather_flow, analize_conversation_flow, cloth_recommendation

def get_start_handler():
    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_choice)],
            WEATHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, weather_flow)],
            CLOTH_RECOMENDATIONS : [MessageHandler(filters.TEXT & ~filters.COMMAND, cloth_recommendation)],
            ANALIZE_CONVERSATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, analize_conversation_flow)]
        },
        fallbacks=[CommandHandler('cancel', cancel_command), CommandHandler('help', help_command)]
    )
    return start_handler