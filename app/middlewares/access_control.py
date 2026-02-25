from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from app.config import Config


class AccessControlMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        config: Config | None = data.get("config")
        if config is None:
            return await handler(event, data)

        # Only enable maintenance filtering when explicit allow-list is provided.
        if not config.maintenance_allow_ids:
            return await handler(event, data)

        allowed = set(config.admin_ids)
        allowed.update(config.maintenance_allow_ids)

        user_id: int | None = None
        if isinstance(event, Message) and event.from_user is not None:
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery) and event.from_user is not None:
            user_id = event.from_user.id

        if user_id is None:
            return None
        if user_id not in allowed:
            return None
        return await handler(event, data)
