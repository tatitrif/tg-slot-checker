"""Модуль для отправки уведомлений о бронировании."""

import logging

logger = logging.getLogger(__name__)


class BaseNotifier:
    """Базовый интерфейс для уведомлений."""

    async def notify(self, data: dict[str, str]) -> None:
        """
        Отправляет уведомление.

        Args:
            data: Данные для уведомления

        Raises:
            NotImplementedError: Метод должен быть реализован в подклассах
        """
        raise NotImplementedError


class TelegramNotifier(BaseNotifier):
    """Отправляет уведомления в Telegram."""

    def __init__(self, client, user_id: int):
        """
        Инициализирует Telegram нотификатор.

        Args:
            client: Клиент Telegram
            user_id: ID пользователя для отправки уведомлений
        """
        self.client = client
        self.user_id = user_id

    async def notify(self, data: dict[str, str]) -> None:
        """
        Отправляет уведомление в Telegram.

        Args:
            data: Данные бронирования для уведомления
        """
        message = (
            f"Запись подтверждена ✅\n\n"
            f"Дата: {data.get('date')}\n"
            f"Время: {data.get('time')}\n"
        )
        await self.client.send_message(self.user_id, message)
        logger.info("Уведомление отправлено пользователю %s", self.user_id)
