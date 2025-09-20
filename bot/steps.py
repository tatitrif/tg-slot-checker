"""Модели Pydantic для описания шагов сценария."""

from typing import Literal
from pydantic import BaseModel


class Step(BaseModel):
    """Базовый шаг сценария."""

    type: str
    description: str


class CommandStep(Step):
    """Шаг отправки команды."""

    type: Literal["command"]
    value: str


class ClickStep(Step):
    """Шаг клика по кнопке."""

    type: Literal["click"]
    search_text: str | None = None
    slot_type: Literal["date", "time"] | None = None
    expected_data: str | None = None
