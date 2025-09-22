from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler

from parser import get_weather, get_currency

BOT_TOKEN = '8401888617:AAHgdeuaOTpHhbSP9uACsE6P7Pzv-E_L544'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text_to_send = 'Привет!'
    await context.bot.send_message(chat_id=chat_id, text=text_to_send)

async def get_data_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = context.args[0]
    parsed_data = get_weather(city)
    await update.message.reply_text(f'Вот погода на текущий момент: \n{parsed_data}')

async def get_data_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = context.args[0]
    parsed_data = get_currency(code)
    if parsed_data:
        await update.message.reply_text(f"Вот курс {code} на текущий момент: \n{parsed_data}")
    else:
        await update.message.reply_text(f'Не удалось найти курс для валюты {code}')

def main():
    print('Запуск...')
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('weather', get_data_weather))
    application.add_handler(CommandHandler('currency', get_data_currency))

    application.run_polling()
    print('Бот остановлен')

if __name__ == '__main__':
    main()

