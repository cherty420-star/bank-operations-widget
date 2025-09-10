# Создадим тестовый файл
echo "# Тестовые данные
test_operations = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2024-03-15T10:30:00.000000'},
    {'id': 2, 'state': 'PENDING', 'date': '2024-03-14T12:15:00.000000'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2024-03-16T08:45:00.000000'}
]

if __name__ == '__main__':
    from src.processing import filter_by_state, sort_by_date
    print('Фильтрация:', filter_by_state(test_operations))
    print('Сортировка:', sort_by_date(test_operations))" > test_processing.py