import os


def get_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, default))
    except ValueError:
        return default


def get_bool(name: str, default: str) -> bool:
    return str(os.getenv(name, default)).lower() == "true"


def get_list(name: str, default: str = "", sep: str = ",") -> tuple:
    return tuple([v for v in os.getenv(name, default).split(sep) if v])


def get_str(name: str, default: str) -> str:
    return os.getenv(name, default)


def get_float(name: str, default: str) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return float(default)


def check_env_vars(*classes) -> None:
    for cls in classes:
        for var in cls.__dict__:
            if var.startswith("__") or var.startswith("_"):
                continue

            if not getattr(cls, var):
                raise ValueError(f"Environment variable {str(var).upper()} is not set.")
