import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
) 
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# ---------- ТЕКСТЫ ----------

WELCOME_TEXT = (
    "🧠 *MED-AI-CORRECTOR*\n\n"
    "Интеллектуальный помощник для медицинских текстов.\n"
    "Отправь текст — я приведу его в клинический вид."
)

KEYBOARD = ReplyKeyboardMarkup(
    [["📝 Исправить текст"], ["ℹ️ О сервисе"]],
    resize_keyboard=True
)

# ---------- ХЕНДЛЕРЫ ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=KEYBOARD, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📝 Исправить текст":
        await update.message.reply_text(
            "✍️ Отправь медицинский текст, я приведу его в корректный вид."
        )
        context.user_data["mode"] = "edit"
        return

    if text == "ℹ️ О сервисе":
        await update.message.reply_text(
            "MED-AI-CORRECTOR — сервис для врачей.\n"
            "Исправляет формулировки, структуру и стиль медицинских документов."
        )
        return

    # основной режим — обработка текста
    if context.user_data.get("mode") == "edit":
        # пока заглушка
        formatted = f"🩺 *Отредактированный текст:*\n\n{text}"
        await update.message.reply_text(formatted, parse_mode="Markdown")
        return

    await update.message.reply_text("Выберите действие из меню 👇")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 MED-AI-CORRECTOR запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
