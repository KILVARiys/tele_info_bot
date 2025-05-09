import asyncio
from aiogram import Bot, Dispatcher

from handlers.base_handlers import router
from sqlite_db import db_start

def on_startup():
    db_start()

async def main():
    bot=Bot(token='7957557222:AAEaY63hZKfg0R8O1kREJp0LaWdA2iRbOVw')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')