from datetime import datetime, timedelta


def get_date_as_totalmobile_formatted_string(days_from_today: int) -> str:
    date = datetime.today() + timedelta(days=days_from_today)
    return format_date_as_totalmobile_formatted_string(date)


def format_date_as_totalmobile_formatted_string(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT00:00:00")
