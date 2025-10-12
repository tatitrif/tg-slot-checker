"""Фабрика для создания шагов сценария из конфигурации."""

import logging
from collections.abc import Callable, Awaitable

from telethon import errors

from .schemas import StepSchema, CommandStep, ClickStep


logger = logging.getLogger(__name__)


class StepFactory:
    """Фабрика для генерации функций шагов из конфигурации."""

    def __init__(self, client, target_entity, booking_data: dict[str, str]):
        """
        Инициализирует фабрику шагов.

        Args:
            client: Клиент Telegram
            target_entity: Целевой entity (бот)
            booking_data: Словарь для хранения данных бронирования
        """
        self.client = client
        self.target = target_entity
        self.booking_data = booking_data

    def create_steps(
        self, steps: list[StepSchema]
    ) -> list[tuple[Callable[[], Awaitable[bool]], str | None]]:
        """
        Преобразует список Pydantic-моделей шагов в исполняемые асинхронные функции.

        Args:
            steps (list[StepSchema]): Список шагов, загруженных и валидированных через Pydantic.

        Returns:
            list[tuple[Callable[[], Awaitable[bool]], str | None]]:
                Список кортежей, где первый элемент — асинхронная функция шага,
                второй — ключ для сохранения данных (например, 'date', 'time', 'confirmation').
        """
        result = []
        for step in steps:
            if isinstance(step, CommandStep):
                step_func = self._create_command_step(step.value, step.description)
                result.append((step_func, None))

            elif isinstance(step, ClickStep):
                step_func = self._create_click_step(
                    search_text=step.search_text,
                    slot_type=step.slot_type,
                    description=step.description,
                    expected_data=step.expected_data,
                )
                result.append((step_func, step.expected_data))

        return result

    def _create_command_step(self, command: str, description: str):
        """Создает шаг для отправки команды."""

        async def command_step():
            logger.info("Выполняем шаг (команда): %s", description or command)
            try:
                await self.client.send_message(self.target, command)
                logger.debug("Команда '%s' отправлена", command)
                return True
            except errors.RPCError as e:
                logger.error("Ошибка RPC при отправке команды: %s", e)
                return False
            except Exception as e:
                logger.error("Неизвестная ошибка при отправке команды: %s", e)
                return False

        return command_step

    def _create_click_step(
        self,
        search_text: str | None,
        slot_type: str | None,
        description: str,
        expected_data: str | None,
    ):
        """Создает шаг для клика по кнопке."""

        async def click_step():
            logger.info(
                "Выполняем шаг (клик): %s", description or search_text or slot_type
            )

            try:
                async for message in self.client.iter_messages(self.target, limit=15):
                    if not message.reply_markup:
                        continue

                    for row_index, row in enumerate(message.reply_markup.rows):
                        for button_index, button in enumerate(row.buttons):
                            button_text = getattr(button, "text", "")

                            if self._match_condition(
                                button_text, search_text, slot_type
                            ):
                                if expected_data:
                                    self.booking_data[description] = button_text
                                    logger.debug(
                                        "Сохранили %s: %s", expected_data, button_text
                                    )

                                logger.info("Нажимаем кнопку: %s", button_text)
                                await message.click(row_index, button_index)
                                return True

                logger.warning("Кнопка для '%s' не найдена", search_text or slot_type)
                return False

            except errors.RPCError as e:
                logger.error("Ошибка RPC при клике: %s", e)
                return False
            except Exception as e:
                logger.error("Неизвестная ошибка при клике: %s", e)
                return False

        return click_step

    @staticmethod
    def _match_condition(
        text: str, search_text: str | None, slot_type: str | None
    ) -> bool:
        """Проверяет условие для кнопки."""
        if not text:
            return False

        if search_text and search_text.lower() in text.lower():
            return True
        if slot_type == "date" and any(ch.isdigit() for ch in text):
            return True
        if slot_type == "time" and (":" in text or "-" in text):
            return True

        return False
