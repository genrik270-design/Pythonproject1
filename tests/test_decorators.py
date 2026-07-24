import pytest
from src.decorators import log


# Тест логирования в консоль (проверяем, что функция просто работает)
def test_log_console():
    @log
    def sample_func(x):
        return x * 2

    assert sample_func(5) == 10


# Тест логирования в файл (проверяем создание файла и запись текста)
def test_log_file(tmp_path):
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def greet(name):
        return f"Hello, {name}"

    greet("Alice")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "[START] Функция 'greet'" in content
    assert "[SUCCESS] Функция 'greet'" in content


# Тест логирования ошибки
def test_log_error(tmp_path):
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def division_by_zero():
        return 1 / 0

    with pytest.raises(ZeroDivisionError):
        division_by_zero()

    content = log_file.read_text(encoding="utf-8")
    assert "[ERROR]" in content
    assert "ZeroDivisionError" in content
    