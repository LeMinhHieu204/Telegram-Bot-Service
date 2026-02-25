# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.config import load_config
from app.db.schema import init_db
from app.handlers import admin, guide, home, mem, profile, services, terms, topup, telegram_view, sepay_group
from app.middlewares.access_control import AccessControlMiddleware
from app.webhooks import create_sepay_app
from app.sepay_polling import run_polling


async def main() -> None:
    load_dotenv()
    config = load_config()
    await init_db(config.db_path)

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    access_control = AccessControlMiddleware()
    dp.message.middleware(access_control)
    dp.callback_query.middleware(access_control)

    dp.include_router(home.router)
    dp.include_router(guide.router)
    dp.include_router(terms.router)
    dp.include_router(profile.router)
    dp.include_router(mem.router)
    dp.include_router(services.router)
    dp.include_router(topup.router)
    dp.include_router(telegram_view.router)
    dp.include_router(sepay_group.router)
    dp.include_router(admin.router)

    app = create_sepay_app(bot, config)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", config.sepay_webhook_port)
    await site.start()

    try:
        asyncio.create_task(run_polling())
        await dp.start_polling(bot, config=config)
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
