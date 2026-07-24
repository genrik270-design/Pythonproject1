import functools
import sys
from typing import Callable, Optional, TypeVar, Any, overload
from typing_extensions import ParamSpec

# Определяем универсальные переменные типов для сохранения сигнатуры функций
P = ParamSpec("P")
R = TypeVar("R")


# 1. Перегрузка для случая без скобок: @log
@overload
def log(filename: Callable[P, R]) -> Callable[P, R]: ...


# 2. Перегрузка для случая с аргументом: @log(filename="app.log")
@overload
def log(filename: Optional[str] = None) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


# Реализация декоратора
def log(filename: Any = None) -> Any:
    # Если декоратор вызван без скобок: @log
    if callable(filename):
        _func = filename
        return log(filename=None)(_func)

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Форматируем входные параметры для вывода при ошибке
            args_str = ", ".join(map(repr, args))
            kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            params = ", ".join(filter(None, [args_str, kwargs_str]))

            # Функция вывода (в файл или консоль)
            def write_log(message: str) -> None:
                if isinstance(filename, str):
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message + "\n")
                else:
                    print(message, file=sys.stderr)

            # 1. Логируем начало
            write_log(f"[START] Функция '{func.__name__}' начала выполнение.")

            try:
                # Выполняем основную функцию
                result = func(*args, **kwargs)

                # 2. Логируем успешный конец и результат
                write_log(f"[SUCCESS] Функция '{func.__name__}' завершена. Результат: {result}")
                return result

            except Exception as e:
                # 3. Логируем ошибку и входные параметры
                error_type = type(e).__name__
                write_log(
                    f"[ERROR] В функции '{func.__name__}' произошла ошибка [{error_type}].\n"
                    f"   Параметры вызова: ({params})\n"
                    f"   Сообщение ошибки: {e}"
                )
                raise  # Пробрасываем ошибку дальше

        return wrapper

    return decorator
