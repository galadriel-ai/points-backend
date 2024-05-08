from datetime import datetime, timezone

timespec: str = "milliseconds"


def execute():
    dt = datetime.now()
    return (dt.astimezone(tz=timezone.utc)
            .isoformat(timespec=timespec)
            .replace("+00:00", "Z"))
