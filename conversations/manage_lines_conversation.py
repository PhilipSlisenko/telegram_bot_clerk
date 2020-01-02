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

CHOOSE_LINE = range(1)


@guarantee_token
def display_lines(update, context):

    url = config['api_url'] + '/clerks/my-lines'
    headers = {"Authorization": "Bearer " + context.user_data.get('token')}
    res = requests.get(url, headers=headers)

    lines_full = res.json()
    lines_names = [x['name'] for x in lines_full]

    buttons = [[KeyboardButton(x)] for x in lines_names] + [[KeyboardButton("🔙 Back")]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    update.message.reply_text("Here are your lines. Choose which one to manage:", reply_markup=keyboard)
    return CHOOSE_LINE


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
    update.message.reply_text('Line creation aborted.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


manage_lines_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r"My lines 📋"), display_lines)],

    states={
        CHOOSE_LINE: [MessageHandler(Filters.text, validate_name)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
