
# Bank Operations Widget

Виджет для работы с банковскими операциями клиента.

## Установка

1. Клонируйте репозиторий:
\\\`\\\`\\\`bash
git clone <ссылка-на-репозиторий>
cd bank-operations-widget-new
\\\`\\\`\\\`

2. Установите зависимости (если есть):
\\\`\\\`\\\`bash
pip install -r requirements.txt
\\\`\\\`\\\`

## Функциональность

### Модуль processing

#### filter_by_state(operations: List[Dict], state: str = 'EXECUTED') -> List[Dict]
Фильтрует список операций по статусу.

**Параметры:**
- \\\`operations\\\`: список словарей с операциями
- \\\`state\\\`: статус для фильтрации (по умолчанию 'EXECUTED')

**Пример:**
\\\`\\\`\\\`python
from src.processing import filter_by_state

operations = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2024-03-15T10:30:00.000000'},
    {'id': 2, 'state': 'PENDING', 'date': '2024-03-14T12:15:00.000000'}
]

executed_ops = filter_by_state(operations, 'EXECUTED')
\\\`\\\`\\\`

#### sort_by_date(operations: List[Dict], reverse: bool = True) -> List[Dict]
Сортирует список операций по дате.

**Параметры:**
- \\\`operations\\\`: список словарей с операциями
- \\\`reverse\\\`: порядок сортировки (True - по убыванию, False - по возрастанию)

**Пример:**
\\\`\\\`\\\`python
from src.processing import sort_by_date

sorted_ops = sort_by_date(operations, reverse=True)
\\\`\\\`\\\`

## Разработка

Проект использует GitFlow. Основные ветки:
- \\\`main\\\` - стабильная версия
- \\\`develop\\\` - разработка
- \\\`feature/*\\\` - новые функции

## Тестирование

Запуск тестов:
\\\`\\\`\\\`bash
python test_processing.py
\\\`\\\`\\\`
" > README.md

## Модуль processing

### filter_by_state()
Фильтрует операции по статусу.

### sort_by_date()
Сортирует операции по дате.