import os
import asyncio

from aiogram import Bot, Dispatcher, types
from bson import ObjectId
from db_ import setup_db

BOT_TOKEN = os.environ.get('BOT_TOKEN')


async def start_handler(event: types.Message):
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )


async def url_handler(event: types.Message):
    db = await setup_db()
    collection = db['shortener']

    user_url = event.text
    url_breakdown_list = user_url.split('://')
    user_url_record = await collection.insert_one({'user_url': url_breakdown_list[1],
                                                   'prefix': url_breakdown_list[0]})
    id_user_url = str(user_url_record.inserted_id)

    await event.answer(id_user_url)


async def show_user_link(event: types.Message):
    db = await setup_db()
    collection = db['shortener']

    id_url = event.text
    try:
        user_url_obj = await collection.find_one({"_id": ObjectId(id_url)})
        prefix_user_url = str(user_url_obj.get('prefix', 'http'))
        user_url = str(user_url_obj.get('user_url'))
        user_url_in_db = prefix_user_url + '://' + user_url

    except BaseException:
        user_url_in_db = "Not found user url"

    await event.answer(user_url_in_db)


async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler, commands={"start", "restart"})
        disp.register_message_handler(url_handler, regexp='http.+')
        disp.register_message_handler(show_user_link, regexp='[a-z0-9]+')
        await disp.start_polling()
    finally:
        await bot.close()


asyncio.run(main())
