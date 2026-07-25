import functools
import sys


def log(filename=None):
    if callable(filename):
        _func = filename
        return log(filename=None)(_func)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_str = ", ".join(map(repr, args))
            kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            params = ", ".join(filter(None, [args_str, kwargs_str]))

            def write_log(message):
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message + "\n")
                else:
                    print(message, file=sys.stderr)

            # Лаконичные и чистые сообщения
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
