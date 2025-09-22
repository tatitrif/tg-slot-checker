"""Модуль для выполнения шагов сценария бронирования."""

import asyncio
import logging
from collections.abc import Callable
from collections.abc import Awaitable

from settings import settings

logger = logging.getLogger(__name__)


async def execute_steps(
    steps: list[tuple[Callable[[], Awaitable[bool]], str | None]],
    step_delay: int = settings.step_delay,
    max_attempts: int = settings.max_attempts,
    restart_delay: int = settings.restart_delay,
) -> bool:
    """Запускает сценарий пошагово, с возможностью повторного запуска всего процесса."""
    for attempt in range(1, max_attempts + 1):
        logger.info("=== Запуск сценария (попытка %d/%d) ===", attempt, max_attempts)
        scenario_failed = False

        for step_index, (step_func, _expected_data) in enumerate(steps, start=1):
            try:
                success = await step_func()
            except Exception as e:
                logger.warning("Шаг %d: исключение: %s", step_index, e)
                success = False

            if success:
                logger.info("Шаг %d выполнен успешно", step_index)
                await asyncio.sleep(step_delay)
                continue

            logger.error("Шаг %d провален. Сценарий будет перезапущен.", step_index)
            scenario_failed = True
            break  # прерываем текущий сценарий

        if not scenario_failed:
            logger.info("Сценарий успешно завершён на попытке %d", attempt)
            return True

        if attempt < max_attempts:
            logger.info("Ждём %d секунд перед перезапуском сценария", restart_delay)
            await asyncio.sleep(restart_delay)

    logger.error("Сценарий не был выполнен успешно после %d попыток", max_attempts)
    return False
