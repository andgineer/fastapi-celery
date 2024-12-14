"""
JSON serialization with precise datetime format control

Usage:
>>> import json
>>> dt = datetime.now()
>>> obj = json.loads(json.dumps({'datetime': dt}, default=json_serial))
>>> obj['datetime'] == dt.isoformat()
True
"""

from datetime import date, datetime


def json_serial(obj):
    """
    Serialize datetime to ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
    (javascript compatible)
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
