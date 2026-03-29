# Отчет по лабораторной работе №2
## Дескрипторы в Python

**Студент:** Панарин Максим Валерьевич  
**Дата:** 29 марта 2026 г.

---

## Цель работы

Изучение механизма дескрипторов в Python, понимание разницы между data-дескрипторами и non-data дескрипторами, применение дескрипторов для валидации атрибутов класса.

---

## Задание

1. Реализовать класс `Task` с валидацией атрибутов через дескрипторы
2. Создать data-дескрипторы для валидации типов и значений
3. Создать non-data дескриптор для демонстрации разницы в поведении
4. Реализовать пользовательские исключения
5. Покрыть код тестами

## Реализация

### Структура проекта

```
Lab2/
├── src/
│   ├── task.py          # Класс Task
│   ├── descriptors.py   # Дескрипторы
│   └── exceptions.py    # Пользовательские исключения
└── tests/
    └── test.py          # Тесты (pytest)
```

### 1. Пользовательские исключения

**Файл:** [src/exceptions.py](src/exceptions.py)

```python
class PriorityError(ValueError):
    """Custom exception for priority value"""
    pass

class StatusError(ValueError):
    """Custom exception for task status"""
    pass
```

Созданы два пользовательских исключения, наследующихся от `ValueError`, для обработки ошибок валидации приоритета и статуса задачи.

### 2. Data-дескрипторы

**Файл:** [src/descriptors.py](src/descriptors.py)

#### TypeDescriptor
```python
class TypeDescriptor:
    """Data-descriptor for validation type"""
    
    def __init__(self, type):
        self.type = type

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError(f"Expected type: {self.type.__name__}")
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)
```

**Назначение:** Валидация типов атрибутов (используется для `id` и `description`)

#### PriorityDescriptor
```python
class PriorityDescriptor:
    """Data-descriptor for validation priority value"""
    
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"Expected int type")
        if not 0 <= value < 6:
            raise PriorityError(f"Priority must be in range: 0-5")
        instance.__dict__[self.name] = value
```

**Назначение:** Валидация приоритета задачи (диапазон 0-5)

#### StatusDescriptor
```python
class StatusDescriptor:
    """Data-descriptor for validation task status"""
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"Expected str type")
        if value not in ("Created", "In_progress", "Completed"):
            raise StatusError(f"Status must be valid")
        instance.__dict__[self.name] = value
```

**Назначение:** Валидация статуса задачи (один из трех допустимых значений)

### 3. Non-data дескриптор

```python
class CreatedAtDescriptor:
    """Non-data Descriptor for creation time"""

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
```

**Назначение:** Демонстрация non-data дескриптора. Не имеет `__set__`, поэтому может быть затенен прямым присваиванием в `__dict__`.

**Ключевое отличие:** 
- Data-дескриптор блокирует прямое изменение через валидацию
- Non-data дескриптор можно затенить: `task._created_at = "new_value"`

### 4. Класс Task

**Файл:** [src/task.py](src/task.py)

```python
class Task:
    """Class for task object with id, description, priority, status and timestamp"""
    
    # Дескрипторы уровня класса
    id = TypeDescriptor(int)
    description = TypeDescriptor(str)
    priority = PriorityDescriptor()
    status = StatusDescriptor()
    _created_at = CreatedAtDescriptor()

    def __init__(self, id, description, priority, status="Created"):
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = datetime.datetime.now().replace(microsecond=0)

    @property
    def is_ready(self):
        """Check if task is ready"""
        return self.status == "Created" and self.priority > 0 and self.id
    
    @property
    def time_from_creation(self):
        """Time since creation"""
        return datetime.datetime.now().replace(microsecond=0) - self._created_at
```

**Особенности:**
- `id`, `description`, `priority`, `status` — защищены data-дескрипторами с валидацией
- `_created_at` — использует non-data дескриптор
- `is_ready` и `time_from_creation` — вычисляемые свойства через `@property`
- Время создания округлено до целых секунд (`replace(microsecond=0)`)

---

## Тестирование

**Файл:** [tests/test.py](tests/test.py)

Реализовано **18 тестов** с использованием `pytest`:

### Покрытие тестов:

1. **TypeDescriptor** (3 теста)
   - Корректная валидация типов
   - Ошибка при неверном типе `id`
   - Ошибка при неверном типе `description`

2. **PriorityDescriptor** (4 теста)
   - Валидные значения 0-5
   - Ошибка при превышении максимума
   - Ошибка при отрицательном значении
   - Ошибка при неверном типе

3. **StatusDescriptor** (3 теста)
   - Валидные статусы
   - Ошибка при невалидном статусе
   - Значение по умолчанию

4. **CreatedAtDescriptor** (2 теста)
   - Установка времени при создании
   - Затенение non-data дескриптора

5. **Task** (4 теста)
   - Создание задачи
   - Свойство `is_ready` (3 сценария)
   - Вычисление `time_from_creation`

6. **Data vs Non-data** (2 теста)
   - Data дескриптор с валидацией
   - Non-data дескриптор с затенением

### Результаты

```bash
$ pytest Lab2/tests/test.py -v
======================== 18 passed ========================
```

Все тесты пройдены успешно

---

## Примеры использования

### Создание задачи

```python
from task import Task

# Корректное создание
task = Task(1, "Implement feature", 3)
print(task.status)  # "Created"
print(task.priority)  # 3
```

### Валидация типов

```python
# Ошибка: неверный тип
task = Task("not_int", "Description", 2)  # TypeError
task.description = 123  # TypeError
```

### Валидация значений

```python
# Ошибка: приоритет вне диапазона
task = Task(1, "Task", 10)  # PriorityError

# Ошибка: неверный статус
task = Task(1, "Task", 2, "Invalid")  # StatusError
```

### Демонстрация data vs non-data

```python
task = Task(1, "Test", 3)

# Data descriptor — валидация работает
task.priority = 999  # PriorityError!

# Non-data descriptor — можно затенить
task._created_at = "shadowed"  # Работает
print(task._created_at)  # "shadowed"
```

### Вычисляемые свойства

```python
task = Task(1, "Task", 4)

print(task.is_ready)  # True
print(task.time_from_creation)  # timedelta(seconds=X)
```

---

## Выводы

В ходе выполнения лабораторной работы:

1. **Изучен протокол дескрипторов** — реализованы методы `__get__`, `__set__`, `__set_name__`

2. **Понята разница между data и non-data дескрипторами:**
   - Data-дескрипторы имеют приоритет и контролируют доступ
   - Non-data дескрипторы могут быть затенены атрибутами экземпляра

3. **Применена валидация через дескрипторы:**
   - Валидация типов (`TypeDescriptor`)
   - Валидация диапазона значений (`PriorityDescriptor`)
   - Валидация набора допустимых значений (`StatusDescriptor`)

4. **Реализованы пользовательские исключения** для специфичных ошибок валидации

5. **Применен принцип разделения интерфейса:**
   - Публичный API (свойства через `@property`)
   - Внутреннее состояние (защищенные атрибуты)

6. **Покрытие тестами** — 18 тестов проверяют все аспекты работы дескрипторов

### Преимущества дескрипторов

- **Переиспользуемость** — один дескриптор можно применять к разным атрибутам
- **Централизованная логика** — валидация в одном месте
- **Декларативный стиль** — понятное объявление атрибутов на уровне класса
- **Контроль доступа** — полный контроль над чтением и записью

