## Функциональность

### Модуль processing

#### filter_by_state(operations: List[Dict], state: str = 'EXECUTED') -> List[Dict]
Фильтрует список операций по статусу.

**Параметры:**
- `operations`: список словарей с операциями
- `state`: статус для фильтрации (по умолчанию 'EXECUTED')

**Возвращает:** отфильтрованный список операций

**Пример:**
```python
from src.processing import filter_by_state

operations = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2024-03-15T10:30:00.000000'},
    {'id': 2, 'state': 'PENDING', 'date': '2024-03-14T12:15:00.000000'}
]

executed_ops = filter_by_state(operations, 'EXECUTED')
```

#### sort_by_date(operations: List[Dict], reverse: bool = True) -> List[Dict]
Сортирует список операций по дате.

**Параметры:**
- `operations`: список словарей с операциями  
- `reverse`: порядок сортировки (True - по убыванию, False - по возрастанию)

**Возвращает:** отсортированный список операций

**Пример:**
```python
from src.processing import sort_by_date

operations = [
    {'date': '2024-03-15T10:30:00.000000', 'amount': 100},
    {'date': '2024-03-16T08:45:00.000000', 'amount': 200}
]

# По убыванию (новые сначала)
sorted_desc = sort_by_date(operations, reverse=True)

# По возрастанию (старые сначала)
sorted_asc = sort_by_date(operations, reverse=False)
```

### Модуль widget

#### mask_account_card(account_info: str) -> str
Маскирует номер карты или счета.

**Пример:**
```python
from src.widget import mask_account_card

masked_card = mask_account_card("Visa Platinum 7000792289606361")
# Результат: "Visa Platinum 7000 79** **** 6361"

masked_account = mask_account_card("Счет 73654108430135874305")  
# Результат: "Счет **4305"
```

#### get_date(date_string: str) -> str
Преобразует дату в формат ДД.ММ.ГГГГ.

**Пример:**
```python
from src.widget import get_date

formatted_date = get_date("2024-03-11T02:26:18.671407")
# Результат: "11.03.2024"
```

## Тестирование

### Запуск тестов
```bash
# Все тесты
pytest

# С отчетом о покрытии
pytest --cov=src --cov-report=html

# Конкретный модуль
pytest tests/test_processing.py -v

Покрытие кода
Запустите pytest --cov=src --cov-report=html

Откройте htmlcov/index.html для просмотра отчета

Требуемое покрытие: >80%

text

## 9. **Сделайте коммиты и создайте PR**

```bash
git add .
git commit -m "Add comprehensive test suite with fixtures and parametrization"
git commit -m "Update README with testing documentation"
git push origin feature/testing


## Модуль generators

### filter_by_currency(transactions, currency) -> Iterator[Dict]
Фильтрует транзакции по валюте и возвращает итератор.

**Параметры:**
- `transactions`: список транзакций
- `currency`: код валюты (например, 'USD', 'RUB', 'EUR')

**Пример:**
```python
from src.generators import filter_by_currency

transactions = [
    {'operationAmount': {'currency': {'code': 'USD'}}},
    {'operationAmount': {'currency': {'code': 'RUB'}}}
]

usd_transactions = filter_by_currency(transactions, 'USD')
for transaction in usd_transactions:
    print(transaction)

transaction_descriptions(transactions) -> Generator[str]
Генератор описаний транзакций.

Пример:

python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for description in descriptions:
    print(description)
card_number_generator(start, end) -> Generator[str]
Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

Параметры:

start: начальный номер (от 1)

end: конечный номер (до 9999999999999999)

Пример:

python
from src.generators import card_number_generator

# Генерация 5 номеров карт
card_numbers = card_number_generator(1, 5)
for number in card_numbers:
    print(number)
# Output: 
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# ...
Тестирование
bash
# Запуск тестов для генераторов
pytest tests/test_generators.py -v

# Проверка покрытия
pytest --cov=src.generators --cov-report=html
Пример использования
python
from src.generators import filter_by_currency, card_number_generator

# Фильтрация транзакций
usd_transactions = list(filter_by_currency(transactions, 'USD'))

# Генерация тестовых номеров карт
test_cards = list(card_number_generator(1000000000000000, 1000000000000005))