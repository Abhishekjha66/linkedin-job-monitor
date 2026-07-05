import asyncio
from telegram_bot import send_message

async def main():
    await send_message("🎉 Frontend Job Alert Bot is working!")

if __name__ == "__main__":
    asyncio.run(main())