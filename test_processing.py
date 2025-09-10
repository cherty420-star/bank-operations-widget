"# Тестовые данные для проверки функций

test_operations = [
    {
        'id': 1,
        'state': 'EXECUTED',
        'date': '2024-03-15T10:30:00.000000',
        'amount': '100.00',
        'description': 'Перевод организации'
    },
    {
        'id': 2,
        'state': 'PENDING',
        'date': '2024-03-14T12:15:00.000000',
        'amount': '200.00',
        'description': 'Перевод со счета на счет'
    },
    {
        'id': 3,
        'state': 'EXECUTED',
        'date': '2024-03-16T08:45:00.000000',
        'amount': '300.00',
        'description': 'Перевод с карты на карту'
    },
    {
        'id': 4,
        'state': 'CANCELED',
        'date': '2024-03-13T16:20:00.000000',
        'amount': '400.00',
        'description': 'Перевод физическому лицу'
    }
]

# Примеры использования
if __name__ == '__main__':
    from src.processing import filter_by_state, sort_by_date

    print('=== Фильтрация по статусу ===')
    executed_ops = filter_by_state(test_operations, 'EXECUTED')
    for op in executed_ops:
        print(f\"ID: {op['id']}, Date: {op['date']}, Amount: {op['amount']}\")

        print('\\n=== Сортировка по дате ===')
        sorted_ops = sort_by_date(test_operations, reverse=True)
        for op in sorted_ops:
            print(f\"ID: {op['id']}, Date: {op['date']}, State: {op['state']}\")" > test_processing.py