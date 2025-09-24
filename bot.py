import os

from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler

from parser import get_weather_new, get_currency, get_currency_all

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text_to_send = 'Привет!'
    await context.bot.send_message(chat_id=chat_id, text=text_to_send)

async def get_data_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите город. Например, /weather Moscow")
        return
    city = context.args[0]
    parsed_data = get_weather_new(city)
    await update.message.reply_text(f'Вот погода на текущий момент: \n{parsed_data}')

async def get_data_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = context.args[0]
    parsed_data = get_currency(code)
    if parsed_data:
        await update.message.reply_text(f"Вот курс {code} на текущий момент: \n{parsed_data}")
    else:
        await update.message.reply_text(f'Не удалось найти курс для валюты {code}')

async def get_data_currency_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parsed_data = get_currency_all()
    if parsed_data:
        await update.message.reply_text(parsed_data)
    else:
        await update.message.reply_text(f'Не удалось найти курс валют')



def main():
    print('Запуск...')
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('weather', get_data_weather))
    application.add_handler(CommandHandler('currency', get_data_currency))
    application.add_handler(CommandHandler('currency_all', get_data_currency_all))

    application.run_polling()
    print('Бот остановлен')

if __name__ == '__main__':
    main()

