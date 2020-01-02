from telegram import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("Create new line ➕")], [KeyboardButton("My lines 📋")]],
    resize_keyboard=True,
    one_time_keyboard=True)
