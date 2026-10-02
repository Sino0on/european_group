import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from decouple import config

from leads_bot.parser import TEMPLATE, parse_lead
from main.amocrm import send_amocrm

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger('leads_bot')

BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='').strip()
CHAT_ID = int(config('TELEGRAM_CHAT_ID', default='0') or 0)

dp = Dispatcher()
dp.message.filter(F.chat.id == CHAT_ID)


@dp.message(Command('start', 'help'))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Отправьте в этот чат лид по шаблону, и он сразу попадёт в AmoCRM.\n"
        "Шаблон — командой /template (скопируйте и заполните).\n"
        "Обязательные поля: <b>Имя</b> и <b>Телефон</b>."
    )


@dp.message(Command('template'))
async def cmd_template(message: Message) -> None:
    await message.answer(f"<pre>{TEMPLATE}</pre>")


@dp.message(F.text)
async def handle_lead(message: Message) -> None:

    data, errors = parse_lead(message.text)
    if 'name' not in data and 'phone' not in data:
        return
    if errors:
        await message.answer(
            "❌ Лид не отправлен:\n• " + "\n• ".join(errors) + "\n\nШаблон: /template"
        )
        return

    user = message.from_user
    data['manager'] = user.full_name + (f" (@{user.username})" if user.username else '')

    ok = await asyncio.to_thread(send_amocrm, data)
    if ok:
        logger.info("Lead sent by %s: %s", user.id, data.get('name'))
        await message.answer(
            f"✅ Лид отправлен в AmoCRM\n<b>{data['name']}</b>, {data['phone']}"
        )
    else:
        logger.error("Failed to send lead from %s: %s", user.id, data)
        await message.answer("⚠️ Не удалось отправить в AmoCRM. Попробуйте ещё раз или сообщите администратору.")


async def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN не задан в .env")
    if not CHAT_ID:
        raise SystemExit("TELEGRAM_CHAT_ID не задан в .env")
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
