import pytest

from src.decorators import log


# 1. Тест логирования в консоль
def test_log_console():
    @log
    def sample_func(x):
        return x * 2

    assert sample_func(5) == 10


# 2. Тест логирования успешного выполнения в файл
def test_log_file(tmp_path):
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def greet(name):
        return f"Hello, {name}"

    greet("Bob")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")

    # Проверяем новые упрощенные строки
    assert "Вызов greet..." in content
    assert "-> greet завершена успешно. Результат: Hello, Bob" in content


# 3. Тест логирования ошибки в файл
def test_log_error(tmp_path):
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")

    # Проверяем новый формат вывода ошибок
    assert "Вызов divide..." in content
    assert "-> ОШИБКА в divide(10, 0): [ZeroDivisionError]" in content
