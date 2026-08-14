import pytest

from src.decorators_typed import log


# Оборачиваем тестовые функции в декоратор без параметров
@log()
def add_numbers(a: int, b: int) -> int:
    return a + b


@log()
def divide_numbers(a: int, b: int) -> float:
    return a / b


# Оборачиваем тестовую функцию в декоратор С ПАРАМЕТРОМ
@log(filename="test_log.txt")
def multiply_numbers(a: int, b: int) -> int:
    return a * b


def test_decorator_runs_successfully():
    """Тест проверяет, что декоратор успешно пропускает через себя вызов функции."""
    result = add_numbers(10, 20)
    assert result == 30


def test_decorator_handles_error():
    """Тест проверяет, что декоратор не мешает пробрасывать ошибку наружу."""
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)


def test_decorator_with_filename():
    """Тест проверяет работу декоратора, если передан параметр filename."""
    result = multiply_numbers(5, 5)
    assert result == 25
