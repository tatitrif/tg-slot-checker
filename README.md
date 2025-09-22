# 🤖🔍 Telegram Slot Checker

Асинхронный **Telegram userbot** для автоматизации записи через целевых ботов.
Проект построен по принципам **SOLID**, поддерживает конфигурацию через **YAML + .env**, использует `telethon` и `pydantic`.

---

## 🚀 Возможности

- **Автоматическое бронирование** слотов по заданному сценарию
- **Гибкая конфигурация** шагов через YAML файл
- **Повторные попытки** при неудачных сценариях
- **Уведомления** об успешном бронировании
- **Асинхронная архитектура** на основе Telethon
- Удобная разработка: **Poetry** для зависимостей и **pre-commit** для линтинга

---

## 📂 Структура проекта

```bash
tg-slot-checker/
├── app/                    # Основное приложение
│   ├── steps/              # Логика работы с шагами
│   │   ├── builder.py      # Построитель шагов из конфигурации
│   │   ├── executor.py     # Исполнитель шагов
│   │   ├── loader.py       # Загрузчик шагов из YAML
│   │   └── schemas.py      # Модели данных шагов
│   ├── bot.py              # Основной класс бота
│   └── notifier.py         # Система уведомлений
├── settings.py             # Конфигурация приложения
├── main.py                 # Точка входа
├── steps.yaml              # Конфиг шагов
├── .env.example            # Пример файла окружения
├── pyproject.toml          # Зависимости Poetry
└── .pre-commit-config.yaml # Хуки для Git
```

## 🚀 Быстрый старт

Прежде чем работать с API Telegram, вам нужно получить собственный API_ID и API_HASH.

1. Войдите в свою учётную запись Telegram на официальном сайте Telegram [https://my.telegram.org/auth](https://my.telegram.org/auth)

2. Нажмите на раздел «Инструменты для разработки API».

3. Появится окно 'Создать новое приложение'. Заполните данные о приложении. Не нужно вводить URL, а первые два поля (Название приложения и Краткое название) в настоящее время можно изменить позже.

4. В конце нажмите 'Создать приложение'. Помните, что ваш хэш API является секретным, и Telegram не позволит вам отозвать его. ❗️ Не публикуйте его нигде в открытом доступе!

Если у вас нет Poetry используйте [инструкцию 1](https://python-poetry.org/docs/#installation) для установки Poetry или [инструкцию 2](https://github.com/python-poetry/install.python-poetry.org).

```bash
# Клонирование репозитория
git clone git@github.com:tatitrif/tg-slot-checker.git
cd tg-slot-checker

# Установка зависимостей через Poetry
poetry install

# Активация виртуального окружения
poetry shell

# Создайте файл .env
cp ./.env.example ./.env

# Создайте файл .env
cp ./steps.yaml.example ./steps.yaml

# Запуск
poetry run python main.py
# 📌 При первом запуске появится сообщение от ТГ "Please enter the code you received:", к вам придет сообщение от **Telegram** нужно его ввести в приложение. Если введете несколько раз неправильный код ваше приложение заблокирует отправку сообщений на сутки
```

## 📋 Конфигурация шагов

### Типы шагов

**CommandStep** - отправка команды

```yaml
- type: command
  value: "/start"
  description: "Запуск процесса записи"
```

**ClickStep** - клик по кнопке

```yaml
- type: click
  search_text: "текст" # Текст для поиска кнопки
  description: "Выбор шага 'текст'"

- type: click
  slot_type: date # Автопоиск даты
  expected_data: date # Сохранить выбранную дату
  description: "Выбор даты"

- type: click
  slot_type: time # Автопоиск времени
  expected_data: time # Сохранить выбранное время
  description: "Выбор времени"
```

### Параметры expected_data

- `date` - сохраняет выбранную дату

- `time` - сохраняет выбранное время

- `confirmation` - сохраняет текст подтверждения

## 🛠️ Используемые технологии

### Development & Tools

- **PyCharm** - IDE для разработки
- **Git & GitHub** - Контроль версий, хостинг репозитория и CI/CD

### Core Technologies

- **Python** - Основной язык программирования
- **Telethon+** - Асинхронная библиотека для Telegram MTProto API
- **AsyncIO** - Асинхронное программирование
- **Pydantic Settings** - Валидация конфигурации

### Code Quality

- **Poetry** - Современный менеджер зависимостей
- **Pre-commit** - Фреймворк для управления pre-commit хуками
- **Ruff** - Молниеносный линтер и форматтер
- **Type Hints** - Полная статическая типизация

#### Pre-commit

```bash

# установить pre-commit на устройство
pip install pre-commit==3.8.0

# установить pre-commit в репозитории
pre-commit install

# добавить pre-commit в git
git add .pre-commit-config.yaml

# выполнение pre-commit без коммита
pre-commit run --all-files

# выполнение коммита без pre-commit
git commit --no-verify -m "<message>"

```

### Poetry

```bash

# старт виртуальной среды shell
poetry shell

# эквивалент установки pip, добавляет этот модуль и зависимости к нему
poetry add <module>

# обновить/установить все зависимости
poetry update

```

## 🤝 Contributing

1. Форкните репозиторий

2. Создайте feature branch (`git checkout -b feature/amazing-feature`)

3. Закоммитьте ваши изменения (`git commit -m 'Add amazing feature`)

4. Запушьте ветку (`git push origin feature/amazing-feature`)

5. Откройте Pull Request

---

## ⚠️ Важное примечание

Этот инструмент предназначен для легального использования. Убедитесь что вы:

- Имеете право на автоматическое взаимодействие с целевым ботом

- Не нарушаете условия использования Telegram API

- Соблюдаете законы вашей страны

- Не используйте для спама или автоматизированных атак

- API ключи и пароль храните в безопасности
