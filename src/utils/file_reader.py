import json
import os
import logging
from typing import List, Dict, Any
from ..logger_config import setup_logger

# Настраиваем логгер для модуля utils
logger = setup_logger('utils.file_reader', 'utils.log', logging.DEBUG)


def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из JSON-файла.

    Args:
        file_path: Путь до JSON-файла

    Returns:
        Список словарей с данными транзакций
    """
    logger.debug(f"Starting to read transactions from: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            error_msg = f"File not found: {file_path}"
            logger.error(error_msg)
            return []

        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем что данные - список
        if isinstance(data, list):
            logger.info(f"Successfully read {len(data)} transactions from {file_path}")
            return data
        else:
            error_msg = f"Invalid data format in {file_path}: expected list, got {type(data)}"
            logger.error(error_msg)
            return []

    except json.JSONDecodeError as e:
        error_msg = f"JSON decode error in {file_path}: {e}"
        logger.error(error_msg)
        return []
    except IOError as e:
        error_msg = f"IO error reading {file_path}: {e}"
        logger.error(error_msg)
        return []
    except Exception as e:
        error_msg = f"Unexpected error reading {file_path}: {e}"
        logger.error(error_msg)
        return []