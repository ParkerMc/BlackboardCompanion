from datetime import datetime, timedelta
from calendar import HTMLCalendar
import calendar
from Attendance.models import Meeting_Day

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(meetingDate__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li> {event.meetingTime} {event.course.courseName}</li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, request, withyear=True):
        events = None
        all_classes = request.user.profile.course.all()
        for course in all_classes:
            # the localCourse.lastScanned and currentDate will be
            # replaced with datetime objects that meet the dates you
            # want
            startTime = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            endTime = datetime.today().replace(day=calendar.monthrange(self.year, self.month)[1], hour=23, minute=59, second=59, microsecond=59)
            temp = Meeting_Day.objects.filter(course= course,meetingDate__range=[startTime, endTime])
            if events is None:
                events = temp
            else:
                events = events | temp

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'

        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'

        return cal
