from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

def to_kst(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        # naive datetime이면 UTC로 간주
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(KST)