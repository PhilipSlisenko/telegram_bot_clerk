from config import config
import requests
from helpers import guarantee_token
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove


@guarantee_token
def start(update, context):
    """ Register clerk and send text what user can do """
    reply = """Hello! This bot allows you to easily create and manage lines. Go ahead and create your first line! 😀"""
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("Create new line ➕")], [KeyboardButton("My lines 📋")]],
        resize_keyboard=True,
        one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_user.id, text=reply, reply_markup=keyboard)


@guarantee_token
def other(update, context):
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())


@guarantee_token
def create_line_prompt(update, context):
    context.bot.send_message(chat_id=update.effective_user.id, text="How do you want your new line to be named?")
