import pytest
import os
import tempfile
from src.decorators import log


class TestDecorators:

    def test_log_to_console_success(self, capsys):
        """Тестирование логирования успешного выполнения в консоль"""

        @log()
        def add(a: int, b: int) -> int:
            return a + b

        result = add(2, 3)

        # Проверяем результат
        assert result == 5

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out

        # Проверяем содержание логов
        assert "add - started" in output
        assert "add - finished" in output
        assert "result: 5" in output

    def test_log_to_file_success(self):
        """Тестирование логирования успешного выполнения в файл"""

        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
            temp_filename = temp_file.name

        try:
            @log(filename=temp_filename)
            def multiply(a: int, b: int) -> int:
                return a * b

            result = multiply(4, 5)

            # Проверяем результат
            assert result == 20

            # Читаем содержимое файла
            with open(temp_filename, 'r', encoding='utf-8') as file:
                log_content = file.read()

            # Проверяем содержание логов
            assert "multiply - started" in log_content
            assert "multiply - finished" in log_content
            assert "result: 20" in log_content

        finally:
            # Удаляем временный файл
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_log_to_console_error(self, capsys):
        """Тестирование логирования ошибки в консоль"""

        @log()
        def divide(a: int, b: int) -> float:
            return a / b

        # Проверяем что исключение пробрасывается
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out

        # Проверяем содержание логов ошибки
        assert "divide - started" in output
        assert "divide - failed" in output
        assert "ZeroDivisionError" in output
        assert "args: (10, 0)" in output

    def test_log_to_file_error(self):
        """Тестирование логирования ошибки в файл"""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
            temp_filename = temp_file.name

        try:
            @log(filename=temp_filename)
            def risky_operation(x: int) -> int:
                if x < 0:
                    raise ValueError("Negative values not allowed")
                return x * 2

            # Проверяем что исключение пробрасывается
            with pytest.raises(ValueError):
                risky_operation(-5)

            # Читаем содержимое файла
            with open(temp_filename, 'r', encoding='utf-8') as file:
                log_content = file.read()

            # Проверяем содержание логов ошибки
            assert "risky_operation - started" in log_content
            assert "risky_operation - failed" in log_content
            assert "ValueError" in log_content
            assert "Negative values not allowed" in log_content
            assert "args: (-5,)" in log_content

        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_log_preserves_function_metadata(self):
        """Тестирование что декоратор сохраняет метаданные функции"""

        @log()
        def sample_function(x: int) -> int:
            """Тестовая функция документация"""
            return x

        # Проверяем сохранение метаданных
        assert sample_function.__name__ == "sample_function"
        assert sample_function.__doc__ == "Тестовая функция документация"

    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (10, -5, 5)
    ])
    def test_log_with_parametrized_functions(self, capsys, a, b, expected):
        """Тестирование декоратора с параметризованными функциями"""

        @log()
        def parametrized_add(x: int, y: int) -> int:
            return x + y

        result = parametrized_add(a, b)
        assert result == expected

        captured = capsys.readouterr()
        output = captured.out

        assert "parametrized_add - started" in output
        assert "parametrized_add - finished" in output
        assert f"result: {expected}" in output