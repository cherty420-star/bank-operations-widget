import pandas as pd


def create_operations_xlsx():
    """Создает Excel файл с операциями."""

    # Данные для Excel файла
    data = [
        {
            'id': 1,
            'state': 'EXECUTED',
            'date': '2024-03-11T02:26:18.671407',
            'amount': 48223.05,
            'currency': 'RUB',
            'description': 'Перевод организации',
            'from': 'Счет 73654108430135874305',
            'to': 'Счет 89685546118890842412'
        },
        {
            'id': 2,
            'state': 'EXECUTED',
            'date': '2024-02-15T08:30:45.123456',
            'amount': 15000.00,
            'currency': 'RUB',
            'description': 'Открытие вклада',
            'from': '',
            'to': 'Счет 41421565395219872341'
        },
        {
            'id': 3,
            'state': 'CANCELED',
            'date': '2024-01-20T14:15:30.789012',
            'amount': 5000.00,
            'currency': 'USD',
            'description': 'Перевод с карты на карту',
            'from': 'Visa Platinum 7000792289606361',
            'to': 'Maestro 1596837868705199'
        },
        {
            'id': 4,
            'state': 'EXECUTED',
            'date': '2023-12-05T10:20:35.456789',
            'amount': 25000.00,
            'currency': 'RUB',
            'description': 'Пополнение счета',
            'from': '',
            'to': 'Счет 65412398745632178945'
        },
        {
            'id': 5,
            'state': 'PENDING',
            'date': '2024-03-20T16:45:12.345678',
            'amount': 7500.50,
            'currency': 'RUB',
            'description': 'Оплата услуг',
            'from': 'MasterCard 1234567812345678',
            'to': 'Счет 98765432109876543210'
        }
    ]

    # Создаем DataFrame
    df = pd.DataFrame(data)

    # Сохраняем в Excel
    df.to_excel('data/operations.xlsx', index=False, engine='openpyxl')
    print("Файл data/operations.xlsx успешно создан!")
    print(f"Создано {len(data)} записей")


if __name__ == "__main__":
    create_operations_xlsx()