"""Модуль для проверки и бронирования слотов через Telegram бота."""

import logging

from telethon import TelegramClient

from settings import settings
from .executor import execute_steps
from .factory import StepFactory
from .notifier import TelegramNotifier

logger = logging.getLogger(__name__)


class CheckerSlotBot:
    """Основной класс: управляет логикой работы с целевым ботом."""

    def __init__(self):
        """Инициализирует клиент Telegram и данные для бронирования."""
        self.client = TelegramClient(
            f"session_{settings.phone_number}",
            settings.api_id,
            settings.api_hash,
            system_version="4.16.30-vxCUSTOM",  # Имитация Android, чтобы не выходил из всех аккаунтов
        )
        self.target_bot = settings.target_bot
        self.booking_data: dict[str, str] = {}

    async def start(self):
        """Запуск клиента и выполнение сценария."""
        await self.client.start(
            phone=settings.phone_number, password=settings.tg_password
        )
        logger.info("Клиент Telegram запущен")

        target = await self.client.get_entity(self.target_bot)

        # Генерация шагов
        factory = StepFactory(self.client, target, self.booking_data)
        steps = factory.create_steps()

        # Выполнение шагов
        success = await execute_steps(
            steps, settings.step_delay, settings.max_attempts, settings.restart_delay
        )

        if success:
            me = await self.client.get_me()
            notifier = TelegramNotifier(self.client, user_id=me.id)
            await notifier.notify(self.booking_data)
