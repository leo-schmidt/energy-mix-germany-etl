from datetime import datetime


def convert_timestamp_to_date(
    timestamp,
    milliseconds=True,
):
    if milliseconds:
        return datetime.fromtimestamp(timestamp / 1000)
    else:
        return datetime.fromtimestamp(timestamp)


def convert_date_to_timestamp(
    date,
    dt_format="%Y-%m-%d %H:%M:%S",
    milliseconds=True,
):
    date_object = datetime.strptime(date, dt_format)
    unix_timestamp = str(int(date_object.timestamp()))
    if milliseconds:
        unix_timestamp *= 1000
    return unix_timestamp
