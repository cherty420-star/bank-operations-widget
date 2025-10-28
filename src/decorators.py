from functools import wraps
import time
from typing import Any, Callable, TypeVar, cast

# Добавляем типизацию для декораторов
F = TypeVar('F', bound=Callable[..., Any])


def log_execution(func: F) -> F:
    """
    Декоратор для логирования времени выполнения функции.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнена за {end_time - start_time:.4f} секунд")
        return result

    return cast(F, wrapper)


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[F], F]:
    """
    Декоратор для повторного выполнения функции при ошибках.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    print(f"Попытка {attempt + 1} не удалась: {e}")

            raise last_exception  # type: ignore

        return cast(F, wrapper)

    return decorator