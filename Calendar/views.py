from calendar import HTMLCalendar, Calendar
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from Calendar.utils import Calendar

@login_required(login_url='/login/')
def add_calendar(request):

  yea= datetime.now().year
  mont = datetime.now().month
  cal = Calendar(yea, mont).formatmonth(request)
  return render(request,
                '../templates/calendar/calendar.html', {
                "calendar": cal
                })

