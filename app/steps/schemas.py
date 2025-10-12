"""Модели Pydantic для описания шагов сценария."""

from typing import Literal, Annotated

from pydantic import BaseModel, Field


class Step(BaseModel):
    """Базовый шаг сценария."""

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
    description: str | None = None
    expected_data: Literal["expected_data"] | None = None


StepSchema = Annotated[CommandStep | ClickStep, Field(discriminator="type")]
