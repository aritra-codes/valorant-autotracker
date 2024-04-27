from datetime import datetime

def compare_datetimes_lazily(a: datetime, b: datetime) -> bool:
    t_kwargs = {"second": 0, "microsecond": 0}

    return a.replace(**t_kwargs) == b.replace(**t_kwargs)