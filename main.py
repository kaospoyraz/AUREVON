import os
import requests
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌌 Aurevon uyandı.\nSorunu yaz, gerisini bana bırak."
    )


async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        await update.message.chat.send_action("typing")

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "AUREVON isimli premium Türkçe AI asistansın. "
                        "Karizmatik, kısa ve akıllı cevaplar ver."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        result = response.json()

        if "choices" not in result:
            await update.message.reply_text(
                f"❌ API Hatası:\n{result}"
            )
            return

        ai_text = result["choices"][0]["message"]["content"]

        if len(ai_text) > 4000:
            ai_text = ai_text[:4000]

        await update.message.reply_text(ai_text)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Hata:\n{e}"
        )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_chat
        )
    )

    print("Bot çalışıyor...")

    app.run_polling()


if __name__ == "__main__":
    main()
