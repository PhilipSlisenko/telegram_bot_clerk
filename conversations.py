import logging
import requests
from config import config
from helpers import guarantee_token

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

NAME_LINE = range(1)


def create_line_prompt(update, context):
    update.message.reply_text("How do you want your new line to be named?", reply_markup=ReplyKeyboardRemove())
    return NAME_LINE


def validate_name(update, context):
    print('entered validate_name')
    line_name = update.message.text
    url = config['api_url'] + '/clerks/create-line'
    headers = {"Authorization": "Bearer " + context.user_data.get('token')}
    payload = {
        "line_name": line_name
    }
    res = requests.post(url, headers=headers, json=payload)
    logger.info("Got response inside validate_name:\nstatus: {}  type: {}\npayload: {}".format(res.status_code, type(res.status_code), res.json()))
    if res.status_code == 409:
        update.message.reply_text("Line name '{}' is already taken 🚫. Choose another name:".format(line_name))
        return NAME_LINE
    if res.status_code == 200:
        keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton("Create new line ➕")], [KeyboardButton("My lines 📋")]],
            resize_keyboard=True,
            one_time_keyboard=True)
        update.message.reply_text(
            "Line '{}' has been successfully created ✅. Now you can manage it by pressing 'My lines 📋'.".format(line_name),
            reply_markup=keyboard)
        return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


name_line_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r'Create new line ➕'), create_line_prompt)],

    states={
        NAME_LINE: [MessageHandler(Filters.text, validate_name)],

        # PHOTO: [MessageHandler(Filters.photo, photo),
        #         CommandHandler('skip', skip_photo)],

        # LOCATION: [MessageHandler(Filters.location, location),
        #            CommandHandler('skip', skip_location)],

        # BIO: [MessageHandler(Filters.text, bio)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
