import functools
import sys


def log(filename=None):
    """Внешняя функция.

    Принимает имя файла и решает, как был вызван декоратор (со скобками или без).
    """

    if callable(filename):
        _func = filename
        return log(filename=None)(_func)

    def decorator(func):
        """Декоратор.
        Принимает целевую функцию `func` и подготавливает для неё обёртку.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """ Функция-обёртка (wrapper).

            Выполняется каждый раз при вызове декорированной функции.
            """
            args_str = ", ".join(map(repr, args))
            kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            params = ", ".join(filter(None, [args_str, kwargs_str]))

            def write_log(message):
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message + "\n")
                else:
                    print(message, file=sys.stderr)
            write_log(f"Вызов {func.__name__}...")

            try:
                result = func(*args, **kwargs)
                write_log(f"-> {func.__name__} завершена успешно. Результат: {result}")
                return result

            except Exception as e:
                error_type = type(e).__name__
                write_log(f"-> ОШИБКА в {func.__name__}({params}): [{error_type}] {e}")
                raise

        return wrapper

    return decorator
