import calendar
from datetime import datetime

class Calendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super().__init__()

    def formatday(self, day, weekday):
        if day == 0:
            return '<td></td>'
        return f'<td class="day" data-day="{day}">{day}</td>'

    def formatweek(self, theweek):
        week = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True):
        cal = f'<table border="1">'
        cal += f'<tr><th colspan="7">{calendar.month_name[self.month]} {self.year}</th></tr>'
        cal += '<tr>' + ''.join(f'<th>{day}</th>' for day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']) + '</tr>'

        for week in self.monthdays2calendar(self.year, self.month):
            cal += self.formatweek(week)

        return cal + '</table>'