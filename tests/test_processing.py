from src.processing import filter_by_state, sort_by_date

# Пример данных
operations = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2024-03-15T10:30:00.000000'},
    {'id': 2, 'state': 'PENDING', 'date': '2024-03-14T12:15:00.000000'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2024-03-16T08:45:00.000000'},
    {'id': 4, 'state': 'CANCELED', 'date': '2024-03-13T16:20:00.000000'}
]

# Фильтрация по статусу
executed_ops = filter_by_state(operations)
print("EXECUTED операции:", executed_ops)

# Сортировка по дате (по убыванию)
sorted_ops = sort_by_date(operations)
print("Отсортированные операции:", sorted_ops)

# Сортировка по возрастанию
sorted_asc = sort_by_date(operations, reverse=False)
print("По возрастанию:", sorted_asc)