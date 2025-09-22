"""Модуль для загрузки шагов сценария из YAML файла."""

import logging

import yaml
from pydantic import TypeAdapter

from .schemas import StepSchema

logger = logging.getLogger(__name__)


def load_steps(path: str) -> list[StepSchema]:
    """
    Загружает и валидирует шаги сценария из YAML файла.

    Args:
        path: Путь к YAML файлу с конфигурацией шагов

    Returns:
        list[StepSchema]: Список валидированных шагов сценария

    Raises:
        FileNotFoundError: Если файл не найден
        PermissionError: Если нет прав доступа к файлу
        yaml.YAMLError: Если ошибка парсинга YAML
        ValueError: Если структура YAML некорректна
    """
    try:
        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("Файл конфигурации не найден: %s", path)
        raise
    except PermissionError:
        logger.error("Нет прав доступа к файлу: %s", path)
        raise
    except yaml.YAMLError as e:
        logger.error("Ошибка парсинга YAML файла %s: %s", path, e)
        raise
    if "steps" not in raw:
        raise ValueError("YAML файл должен содержать ключ 'steps' со списком шагов")

    steps_data = raw.get("steps", [])
    adapter = TypeAdapter(list[StepSchema])
    return adapter.validate_python(steps_data)
