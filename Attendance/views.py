import re
from datetime import datetime, timedelta, date, time
import math, random, string
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import messages
from Attendance.models import Meeting_Day
from Enrolled_Classes.models import Enrolled_Class
from django.contrib.auth.decorators import login_required


def checkInput(start, end, meetTime, midday):
    if len(start) < 8 or len(start) > 10 or len(end) < 8 or len(end) > 10:
        return False, start, end, meetTime

    try:

        datePattern = re.compile("(\d{1,2})\/(\d{1,2})\/(\d{4})")
        timePattern = re.compile("(\d{1,2})\:(\d{1,2})")
        datePattern.match(start)
        datePattern.match(end)
        timePattern.match(meetTime)
    except:
        return False, start, end, meetTime

    month_day = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    parseStart = datePattern.search(start)
    parseEnd = datePattern.search(end)
    parseTime = timePattern.search(meetTime)
    if int(parseStart.group(1)) < 1 or int(parseStart.group(1)) > 12:
        return False, start, end, meetTime
    if int(parseEnd.group(1)) < 1 or int(parseEnd.group(1)) > 12:
        return False, start, end, meetTime
    if int(parseStart.group(2)) < 0 or int(parseStart.group(2)) > month_day[int(parseStart.group(1))]:
        return False, start, end, meetTime
    if int(parseEnd.group(2)) < 0 or int(parseEnd.group(2)) > month_day[int(parseEnd.group(1))]:
        return False, start, end, meetTime
    if int(parseStart.group(3)) > int(datetime.now().year)+1 or int(parseStart.group(3)) < int(datetime.now().year):
        return False, start, end, meetTime
    if int(parseEnd.group(3)) > datetime.now().year+1 or int(parseEnd.group(3)) < datetime.now().year-1:
        return False, start, end, meetTime
    if int(parseTime.group(1)) < 0 or int(parseTime.group(1)) > 12:
        return False, start, end, meetTime
    if int(parseTime.group(2)) < 1 or int(parseTime.group(2)) > 59:
        return False, start, end, meetTime

    if midday == "PM" and parseTime.group(1) != 12:
        hour = int(parseTime.group(1))+12
    elif midday == "AM" and parseTime.group(1) == 12:
        hour = int(parseTime.group(1))-12
    else:
        hour = int(parseTime.group(1))
    start = date(int(parseStart.group(3)), int(parseStart.group(1)), int(parseStart.group(2)))
    end = date(int(parseEnd.group(3)), int(parseEnd.group(1)), int(parseEnd.group(2)))
    if end < start:
        return False, start, end, meetTime
    meetTime = time(hour=hour, minute=int(parseTime.group(2)))
    return True, start, end, meetTime


@login_required(login_url='/login/')
def class_settings_view(request, pk):
    def_group = ""
    all_groups = request.user.groups.all()
    for group in all_groups:
        def_group = group.name

    if def_group == "Professor":
        template = loader.get_template('attendance/classSettings.html')
        localCourse = Enrolled_Class.objects.get(id=pk)

        if request.method == 'POST':
            start = request.POST.get('start', "")
            start = start[5:].replace("-", "/")+"/"+start[0:4]
            end = request.POST.get('end', "")
            end = end[5:].replace("-", "/") + "/" + end[0:4]
            time = request.POST.get('time', "")
            midday = "AM"
            if len(time) > 4 and int(time[0:2]) > 12:
                time = str(int(time[0:2])-12) + time[2:]
                midday = "PM"
            valid, start, end, time = checkInput(start, end, time, midday)

            if valid:
                if start != localCourse.startDate or end != localCourse.endDate or time != localCourse.meetingTime:
                    localCourse.startDate = start
                    localCourse.endDate = end
                    localCourse.meetingTime = time

                    month_day = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    i = start.month
                    count = month_day[i]-start.day
                    i += 1
                    while i < end.month:
                        count += month_day[i]
                        i += 1
                    count += end.day
                    weeks = math.ceil(float(count/7))

                    all_meeting_days = Meeting_Day.objects.filter(course=localCourse)
                    dateTrack = start
                    excess_meetings = len(all_meeting_days)-weeks*2

                    while excess_meetings < 0:
                        new_meeting_day = Meeting_Day.objects.create(course=localCourse)
                        new_meeting_day.save()
                        excess_meetings += 1

                    all_meeting_days = Meeting_Day.objects.filter(course=localCourse)
                    i = -1

                    for meeting_day in all_meeting_days:
                        if i == -1:
                            letters = string.ascii_letters + string.digits
                            randomize = ''.join(random.choice(letters) for i in range(10))
                            meeting_day.meetingDate = dateTrack.strftime("%b. %d, %Y")
                            meeting_day.meetingTime = time
                            meeting_day.randomString = randomize
                            meeting_day.save()
                        elif i%2 == 0 and weeks > 0:
                            dateTrack += timedelta(days=2)
                            randomize = ''.join(random.choice(letters) for i in range(10))
                            meeting_day.meetingDate = dateTrack.strftime("%b. %d, %Y")
                            meeting_day.meetingTime = time
                            meeting_day.randomString = randomize
                            meeting_day.save()
                        elif i%2 == 1 and weeks > 0:
                            dateTrack += timedelta(days=5)
                            randomize = ''.join(random.choice(letters) for i in range(10))
                            meeting_day.meetingDate = dateTrack.strftime("%b. %d, %Y")
                            meeting_day.meetingTime = time
                            meeting_day.randomString = randomize
                            weeks -= 1
                            meeting_day.save()
                        else:
                            Meeting_Day.objects.filter(id=meeting_day.id).delete()
                        i += 1

                    return redirect("/class/")
            elif start != "" and end != "" and time != "":
                messages.error(request, "Make sure that end date is not before start date. (Note year must be current)")
            context = {"class": localCourse}

    else:
        context = {}
        template = loader.get_template('attendance/permissionDenial.html')

    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def class_take_attendance_view(request, pk):
    template = loader.get_template('attendance/TakeAttendance.html')
    localCourse = Enrolled_Class.objects.get(id=pk)
    context = {"class": localCourse}
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def class_attendance_view(request, pk):
    def_group = ""
    all_groups = request.user.groups.all()
    for group in all_groups:
        def_group = group.name

    if def_group == "Professor":

        localCourse = Enrolled_Class.objects.get(id=pk)
        all_meeting_days = Meeting_Day.objects.filter(course=localCourse)
        if all_meeting_days:
            template = loader.get_template('attendance/Attendance.html')

            meeting = Meeting_Day.objects.filter(course=localCourse, meetingDate=request.GET.get('meeting_dates'))
            if meeting:
                presentCount = len(meeting[0].present.all())
                lateCount = len(meeting[0].late.all())
                absentCount = len(meeting[0].absent.all())
                selectedOption = meeting[0].meetingDate
            else:
                presentCount = len(all_meeting_days[0].present.all())
                lateCount = len(all_meeting_days[0].late.all())
                absentCount = len(all_meeting_days[0].absent.all())
                selectedOption = all_meeting_days[0].meetingDate
            context = {"class": localCourse,
                        "Meeting_Days": all_meeting_days,
                        "selected_option": selectedOption,
                        "present_count": presentCount,
                        "late_count": lateCount,
                        "absent_count": absentCount}
        else:
            template = loader.get_template('attendance/UpdateSettings.html')
            context = {}
    else:
        context = {}
        template = loader.get_template('attendance/permissionDenial.html')

    return HttpResponse(template.render(context, request))