import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from marshmallow import pprint
import json
import handlers
from config import config
from conversations import name_line_conv_handler
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)

token = config['bot_token']
# bot = telegram.Bot(token=token)
# # print(bot.get_me())

updater = Updater(token=token, use_context=True)
updater.start_polling()

dispatcher = updater.dispatcher


start_handler = CommandHandler('start', handlers.start)
dispatcher.add_handler(start_handler)

other_handler = CommandHandler('other', handlers.other)
dispatcher.add_handler(other_handler)

# create_line_prompt_handler = MessageHandler(Filters.regex(r'Create new line ➕'), handlers.create_line_prompt)
# dispatcher.add_handler(create_line_prompt_handler)

dispatcher.add_handler(name_line_conv_handler)
