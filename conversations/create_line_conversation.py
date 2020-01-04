import logging

import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from config import config
from helpers import guarantee_token
from keyboards import main_keyboard

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

NAME_LINE = range(1)


def create_line_prompt(update, context):
    update.message.reply_text("How do you want your new line to be named?\n"
                              "If you don't want to create new line type /cancel", reply_markup=ReplyKeyboardRemove())
    return NAME_LINE


@guarantee_token
def validate_name(update, context):
    line_name = update.message.text
    url = config['api_url'] + '/clerks/create-line'
    headers = {"Authorization": "Bearer " + context.user_data.get('token')}
    payload = {"line_name": line_name}
    res = requests.post(url, headers=headers, json=payload)

    logger.info("Got response inside validate_name:\nstatus: {}  type: {}\npayload: {}".format(res.status_code, type(res.status_code), res.json()))

    if res.status_code == 409:
        update.message.reply_text("Line name '{}' is already taken 🚫. Choose another name:".format(line_name))
        return NAME_LINE

    if res.status_code == 200:
        update.message.reply_text(
            "Line '{}' has been successfully created ✅. Now you can manage it by pressing 'My lines 📋'.".format(line_name),
            reply_markup=main_keyboard)
        return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Line creation cancelled.',
                              reply_markup=main_keyboard)

    return ConversationHandler.END


create_line_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r'Create new line ➕'), create_line_prompt)],

    states={
        NAME_LINE: [MessageHandler(Filters.text, validate_name)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
