import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Настраивает логгер для модуля.

    Args:
        name: Имя логгера (обычно __name__ модуля)
        log_file: Имя файла для записи логов
        level: Уровень логирования

    Returns:
        Настроенный логгер
    """
    # Создаем папку logs если её нет
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Полный путь к файлу логов
    log_path = os.path.join(log_dir, log_file)

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Проверяем чтобы хэндлеры не дублировались
    if logger.handlers:
        logger.handlers.clear()

    # Создаем formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Создаем file handler (перезаписываем файл при каждом запуске)
    file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Добавляем handler к логгеру
    logger.addHandler(file_handler)

    return logger