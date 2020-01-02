import requests
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove

from config import config
from helpers import guarantee_token
from keyboards import main_keyboard


@guarantee_token
def start(update, context):
    """ Register clerk and send text what user can do """
    reply = """Hello! This bot allows you to easily create and manage lines. Go ahead and create your first line! 😀"""
    context.bot.send_message(chat_id=update.effective_user.id, text=reply, reply_markup=main_keyboard)


@guarantee_token
def other(update, context):
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())


@guarantee_token
def create_line_prompt(update, context):
    context.bot.send_message(chat_id=update.effective_user.id, text="How do you want your new line to be named?")
