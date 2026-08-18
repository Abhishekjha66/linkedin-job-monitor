import os
import json
import asyncio

from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Comma-separated Telegram chat IDs from GitHub Secret / .env
CHAT_IDS = os.getenv("CHAT_IDS", "")

USERS_FILE = "data/telegram_users.json"


def load_users():
    users = []

    # Load users saved locally
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)

        except (json.JSONDecodeError, FileNotFoundError):
            users = []

    # Add users from CHAT_IDS environment variable
    if CHAT_IDS:
        for chat_id in CHAT_IDS.split(","):
            chat_id = chat_id.strip()

            if chat_id:
                try:
                    chat_id = int(chat_id)

                    if chat_id not in users:
                        users.append(chat_id)

                except ValueError:
                    print(
                        f"Invalid CHAT_ID ignored: {chat_id}",
                        flush=True
                    )

    return users


def save_user(chat_id):
    os.makedirs("data", exist_ok=True)

    users = load_users()

    if chat_id not in users:
        users.append(chat_id)

        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)

        print(
            f"Registered Telegram user: {chat_id}",
            flush=True
        )

    else:
        print(
            f"Telegram user already registered: {chat_id}",
            flush=True
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    print(
        f"USER CHAT ID: {chat_id}",
        flush=True
    )

    save_user(chat_id)

    await update.message.reply_text(
        "✅ Welcome to Fresher Job Alert!\n\n"
        "You are registered successfully.\n\n"
        "🚀 You will now receive matching fresher job alerts."
    )


async def send_message(text):
    users = load_users()

    # Diagnostic information for GitHub Actions
    print(
        f"TELEGRAM USERS: {users}",
        flush=True
    )

    if not users:
        print(
            "No Telegram users registered.",
            flush=True
        )
        return

    bot = Bot(token=BOT_TOKEN)

    for chat_id in users:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )

            print(
                f"Alert sent to {chat_id}",
                flush=True
            )

        except Exception as e:
            print(
                f"Failed to send alert to {chat_id}: {e}",
                flush=True
            )


async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()

    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(run_bot())