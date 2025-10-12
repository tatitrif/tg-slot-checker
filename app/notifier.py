"""Модуль уведомлений с гибкой фабрикой и типизацией."""

import logging
from typing import Any, Protocol, runtime_checkable, TypeVar

from telethon import TelegramClient

logger = logging.getLogger(__name__)

__all__ = ["NotifierRegistry"]

T = TypeVar("T", bound="Notifier")


@runtime_checkable
class Notifier(Protocol):
    """Интерфейс для любых уведомителей."""

    async def notify(self, data: dict[str, str]) -> None:
        """Отправляет уведомление."""
        ...


class NotifierRegistry:
    """Регистрирует уведомители и создает их экземпляры."""

    _registry: dict[str, type[T]] = {}

    @classmethod
    def register(cls, name: str):
        """Декоратор для регистрации уведомителя."""

        def wrapper(notifier_cls: type[T]) -> type[T]:
            if name in cls._registry:
                raise ValueError(f"Notifier '{name}' уже зарегистрирован")
            cls._registry[name] = notifier_cls
            logger.debug("Notifier '%s' зарегистрирован", name)
            return notifier_cls

        return wrapper

    @classmethod
    def create(cls, name: str, **kwargs: Any) -> T:
        """Создает экземпляр уведомителя по имени."""
        try:
            notifier_cls = cls._registry[name]
        except KeyError as e:
            raise ValueError(f"Неизвестный тип уведомителя: {name}") from e
        return notifier_cls(**kwargs)


@NotifierRegistry.register("telegram")
class TelegramNotifier:
    """Отправляет уведомления в Telegram."""

    def __init__(self, sender: TelegramClient, recipient: int) -> None:
        """
        Инициализирует Telegram нотификатор.

        Args:
            sender (TelegramClient): Клиент Telegram для отправки сообщений.
            recipient (int): Список ID получателей.
        """
        self._client = sender
        self._recipient = recipient

    async def notify(self, data: dict[str, str]) -> None:
        lines = [f"{key.capitalize()}: {value}" for key, value in data.items()]
        message = "Запись подтверждена ✅\n\n" + "\n".join(lines)

        await self._client.send_message(self._recipient, message)
        logger.info("Уведомление отправлено пользователю %s", self._recipient)
