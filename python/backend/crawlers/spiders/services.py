from datetime import datetime

def _month_to_int(month: str):
    if month=='января': return 1
    if month=='февраля': return 2
    if month=='марта': return 3
    if month=='апреля': return 4
    if month=='мая': return 5
    if month=='июня': return 6
    if month=='июля': return 7
    if month=='августа': return 8
    if month=='сентября': return 9
    if month=='октября': return 10
    if month=='ноября': return 11
    if month=='декабря': return 12
    
def to_datetime(date: str) -> datetime:
    date = date.split()
    day = int(date[0])
    month = int(_month_to_int(date[1]))
    year = int(date[2])
    hours=date[-1].split(':')
    response = datetime(year, month, day, int(hours[0]), int(hours[1]))
    return response
