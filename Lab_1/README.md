# Лабораторная работа №1. Источники задач и контракты

## Описание

Проект демонстрирует использование duck typing и контрактного программирования на примере системы приёма задач из различных источников. Задачи могут поступать из разных источников, не связанных наследованием, но обязанных реализовывать единый поведенческий контракт.

## Архитектура

Проект использует `typing.Protocol` для описания контракта `GetTasks`, который требует наличия метода `get_tasks() -> list[dict]`. Все источники задач независимы друг от друга и реализуют этот контракт без общего базового класса.

### Источники задач

- **MachineGen** - генерирует задачи программно
- **JsonGen** - загружает задачи из JSON файла
- **ApiGen** - имитирует получение задач через API

## Структура проекта

```
Lab_1_python_2_sem/
├── DATA/
│   └── tasks.json          # JSON файл с задачами
├── src/
│   ├── generators.py       # Классы источников задач
│   ├── protocol.py         # Протокол GetTasks и функция get_all_tasks
│   └── main.py            # Точка входа
├── tests/                  # Тесты (в разработке)
└── README.md
```

## Использование

```python
from generators import ApiGen, MachineGen, JsonGen
from protocol import get_all_tasks
import os

# Создаём источники задач
api_gen = ApiGen()
machine_gen = MachineGen(10)
json_gen = JsonGen("DATA/tasks.json")

# Собираем все задачи
all_tasks = get_all_tasks([api_gen, machine_gen, json_gen])

# Работаем с задачами
for task in all_tasks:
    print(f"Task {task['id']}: {task['payload']}")
```

## Запуск

```bash
# Активировать виртуальное окружение
source .venv/bin/activate  # или активация через VS Code

# Запустить программу
python src/main.py
```

## Требования

- Python 3.10+
- Зависимости указаны в `requirements.txt` и `pyproject.toml`

## Особенности реализации

- Использование `typing.Protocol` для описания контракта
- Runtime-проверка через `@runtime_checkable` и `isinstance()`
- Отсутствие общего базового класса - каждый источник независим
- Возможность добавления новых источников без изменения существующего кода
- Полная типизация с аннотациями типов
