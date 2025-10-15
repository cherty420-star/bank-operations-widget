import logging
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с информацией о транзакциях

    Raises:
        FileNotFoundError: Если файл не найден
        pd.errors.EmptyDataError: Если файл пуст
        Exception: При других ошибках чтения файла
    """
    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict('records')
        logger.info(f"Успешно прочитано {len(transactions)} транзакций из CSV-файла")
        return transactions
    except FileNotFoundError:
        logger.error(f"CSV-файл не найден: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"CSV-файл пуст: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV-файла {file_path}: {str(e)}")
        raise


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла.

    Args:
        file_path (str): Путь к Excel-файлу с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с информацией о транзакциях

    Raises:
        FileNotFoundError: Если файл не найден
        Exception: При других ошибках чтения файла
    """
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict('records')
        logger.info(f"Успешно прочитано {len(transactions)} транзакций из Excel-файла")
        return transactions
    except FileNotFoundError:
        logger.error(f"Excel-файл не найден: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel-файла {file_path}: {str(e)}")
        raise