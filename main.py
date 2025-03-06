import logging
from telegram.ext import (Application)

from settings import TELEGRAM_BOT_TOKEN
from bot.handlers.start_handler import get_start_handler
from db.main import init_db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    init_db()
    
    start_handler = get_start_handler()

    application.add_handler(start_handler)
    application.run_polling()

if __name__ == '__main__':
    main()