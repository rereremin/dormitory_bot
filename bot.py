import csv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import nest_asyncio

nest_asyncio.apply()
TOKEN = '8410913524:AAGsRJIgW_EYxnjIMvYGaBhGImdetOZLtrA'
CSV_FILE = 'dataset.csv'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет, пришли номер своего электронного студенческого билета (можно посмотреть в лк), чтобы посмотреть баллы за поселение. Если нет доступа в лк, то обратись к @sazonova_olg или @rh0dium')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text.strip()


    if not user_input.isdigit():
        await update.message.reply_text('Ошибка: ID должен быть числом. Пожалуйста, введите корректный номер студенческого билета. Если по техническим причинам ')
        return

    query_id = int(user_input)

    found = False
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if 'ID' not in reader.fieldnames:
                await update.message.reply_text('Ошибка: Файл базы данных не содержит столбец "ID". Обратитесь к администратору.')
                return

            for row in reader:

                try:
                    db_id = int(row['ID'].strip())

                    if db_id == query_id:
                        response_lines = [
                            f"Номер студенческого {query_id}:",
                            f"Сумма: {row['sum']}",
                            f"Спорт: {row['sport']}",
                            f"Наука: {row['science']}",
                            f"Студсовет: {row['social']}",
                        ]

                        if float(row['purity']) != 0:
                            response_lines.append(f"Чистота: {row['purity']}")
                        response_lines.append(f"Учеба: {row['marks_clear']}")

                        response = "\n".join(response_lines)
                        await update.message.reply_text(response)
                        found = True
                        break
                except ValueError:

                    continue

        if not found:
            await update.message.reply_text(f'Запись для ID {query_id} не найдена. Проверьте номер или обратитесь к @sazonova_olg или @rh0dium.')
    except FileNotFoundError:
        await update.message.reply_text('Ошибка: Файл базы данных не найден. Обратитесь к администратору.')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}. Обратитесь к @sazonova_olg или @rh0dium.')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()