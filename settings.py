"""Модуль для работы с настройками приложения и конфигурацией шагов."""

import yaml
from pydantic import Field, field_validator
from pydantic import TypeAdapter
from pydantic_settings import BaseSettings, SettingsConfigDict

from bot.schemas import StepSchema


class Settings(BaseSettings):
    """
    Настройки приложения.

    Эти параметры могут быть настроены с помощью переменных окружения. Все настройки
    валидируются при создании экземпляра класса.
    """

    api_id: int = Field(
        ..., description="Идентификатор API Telegram (положительное целое число"
    )
    api_hash: str = Field(..., description="Хэш API Telegram (минимум 10 символов")

    phone_number: str = Field(..., description="Номер телефона аккаунта Telegram")
    tg_password: str = Field(..., description="Пароль двухфакторной аутентификации")
    target_bot: str = Field(..., description="Username целевого бота для мониторинга")
    step_delay: int | None = Field(1, description="Задержка между шагами в секундах")
    max_attempts: int | None = Field(
        1, description="Максимальное число попыток пройти сценарий"
    )
    restart_delay: int | None = Field(
        20 * 60, description="Задержка перед перезапуском сценария"
    )

    steps_file: str = Field("steps.yaml", description="Путь к файлу с шагами сценария")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        """Валидируем номер телефона (+ и цифры)."""
        if not v.startswith("+") or not v[1:].isdigit():
            raise ValueError(
                "Номер телефона должен начинаться с + и содержать только цифры"
            )
        return v

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


def load_steps(path: str) -> list[StepSchema]:
    """Загружает шаги из YAML файла."""
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    steps_data = raw.get("steps", [])
    adapter = TypeAdapter(list[StepSchema])
    return adapter.validate_python(steps_data)


settings = Settings()
