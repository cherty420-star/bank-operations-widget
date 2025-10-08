import datetime
from typing import Any, Callable, Optional
from functools import wraps


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: Имя файла для записи логов. Если None - вывод в консоль.

    Returns:
        Декорированную функцию
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Время начала выполнения
            start_time = datetime.datetime.now()
            func_name = func.__name__

            # Логируем начало выполнения
            log_message = f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - {func_name} - started\n"

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное завершение
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                success_message = (
                    f"{end_time.strftime('%Y-%m-%d %H:%M:%S')} - {func_name} - finished "
                    f"[execution time: {execution_time:.2f}s] - result: {result}\n"
                )
                log_message += success_message

                # Записываем лог
                _write_log(log_message, filename)

                return result

            except Exception as e:
                # Логируем ошибку
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                error_message = (
                    f"{end_time.strftime('%Y-%m-%d %H:%M:%S')} - {func_name} - failed "
                    f"[execution time: {execution_time:.2f}s] - error: {type(e).__name__}: {e} - "
                    f"args: {args}, kwargs: {kwargs}\n"
                )
                log_message += error_message

                # Записываем лог
                _write_log(log_message, filename)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """
    Записывает сообщение в файл или выводит в консоль.

    Args:
        message: Сообщение для логирования
        filename: Имя файла для записи (None для вывода в консоль)
    """
    if filename:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(message)
    else:
        print(message, end='')