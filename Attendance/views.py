import re
from datetime import datetime, timedelta, date, time
import math, random, string
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import messages
from Attendance.models import Meeting_Day
from BlackboardCompanion import settings
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
    if int(parseStart.group(3)) > int(datetime.now().year) + 1 or int(parseStart.group(3)) < int(datetime.now().year):
        return False, start, end, meetTime
    if int(parseEnd.group(3)) > datetime.now().year + 1 or int(parseEnd.group(3)) < datetime.now().year - 1:
        return False, start, end, meetTime
    if int(parseTime.group(1)) < 0 or int(parseTime.group(1)) > 12:
        return False, start, end, meetTime
    if int(parseTime.group(2)) < 1 or int(parseTime.group(2)) > 59:
        return False, start, end, meetTime

    if midday == "PM" and parseTime.group(1) != 12:
        hour = int(parseTime.group(1)) + 12
    elif midday == "AM" and parseTime.group(1) == 12:
        hour = int(parseTime.group(1)) - 12
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
            start = start[5:].replace("-", "/") + "/" + start[0:4]
            end = request.POST.get('end', "")
            end = end[5:].replace("-", "/") + "/" + end[0:4]
            time = request.POST.get('time', "")
            midday = "AM"
            if len(time) > 4 and int(time[0:2]) > 12:
                time = str(int(time[0:2]) - 12) + time[2:]
                midday = "PM"
            valid, start, end, time = checkInput(start, end, time, midday)

            if valid:
                if start != localCourse.startDate or end != localCourse.endDate or time != localCourse.meetingTime:
                    localCourse.startDate = start
                    localCourse.endDate = end
                    localCourse.meetingTime = time

                    month_day = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    i = start.month
                    count = month_day[i] - start.day
                    i += 1
                    while i < end.month:
                        count += month_day[i]
                        i += 1
                    count += end.day
                    weeks = math.ceil(float(count / 7))

                    all_meeting_days = Meeting_Day.objects.filter(course=localCourse)
                    dateTrack = start
                    new_meetings = weeks * 2+2
                    for meeting_day in all_meeting_days:
                        Meeting_Day.objects.filter(id=meeting_day.id).delete()
                    while new_meetings > 0:
                        new_meeting_day = Meeting_Day.objects.create(course=localCourse)
                        new_meeting_day.save()
                        new_meetings -= 1

                    all_meeting_days = Meeting_Day.objects.filter(course=localCourse)
                    i = -1

                    for meeting_day in all_meeting_days:
                        if i == -1:
                            letters = string.ascii_letters + string.digits
                            randomize = ''.join(random.choice(letters) for i in range(10))
                            meeting_day.meetingDate = dateTrack
                            meeting_day.meetingString = dateTrack.strftime("%b. %d, %Y")
                            meeting_day.meetingTime = time
                            meeting_day.randomString = randomize
                            for student in localCourse.students.all():
                                meeting_day.not_applicable.add(student)
                            meeting_day.save()
                        elif i % 2 == 0 and weeks > 0:
                            dateTrack += timedelta(days=2)
                            randomize = ''.join(random.choice(letters) for i in range(10))
                            meeting_day.meetingDate = dateTrack
                            meeting_day.meetingString = dateTrack.strftime("%b. %d, %Y")
                            meeting_day.meetingTime = time
                            meeting_day.randomString = randomize
                            for student in localCourse.students.all():
                                meeting_day.not_applicable.add(student)
                            meeting_day.save()
                        elif i % 2 == 1 and weeks > 0:
                            dateTrack += timedelta(days=5)
                            randomize = ''.join(random.choice(letters) for i in range(10))
                            meeting_day.meetingDate = dateTrack
                            meeting_day.meetingString = dateTrack.strftime("%b. %d, %Y")
                            meeting_day.meetingTime = time
                            meeting_day.randomString = randomize
                            for student in localCourse.students.all():
                                meeting_day.not_applicable.add(student)
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

    else:
        context = {}
        template = loader.get_template('attendance/permissionDenial.html')

    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def class_take_attendance_view(request, pk):
    template = loader.get_template('attendance/TakeAttendance.html')
    localCourse = Enrolled_Class.objects.get(id=pk)
    todayDate = date.today()
    meeting = Meeting_Day.objects.filter(course=localCourse, meetingString=todayDate.strftime("%b. %d, %Y"))
    isPresent = False
    isLate = False
    isAbsent = False

    if meeting and request.method == "GET":
        inCourse = False
        all_courses = request.user.profile.course.all()
        for course in all_courses:
            if course == localCourse:
                inCourse = True
        if inCourse:
            found = True
            print(meeting[0].randomString)
            presentList = meeting[0].present.all()
            lateList = meeting[0].late.all()
            absentList = meeting[0].absent.all()
            if request.GET.get("attendance_code") == meeting[0].randomString:
                if request.user in presentList or request.user in lateList or request.user in absentList:
                    messages.info(request,
                                  "Your Attendance has already been taken for the " + meeting[
                                      0].meetingString + " meeting.")
                else:
                    currentTime = datetime.now()
                    tooEarly = datetime.combine(date.today(), meeting[0].meetingTime) + timedelta(minutes=-5, seconds=-1)
                    lowerPresent = datetime.combine(date.today(), meeting[0].meetingTime) + timedelta(minutes=-5)
                    upperPresent = datetime.combine(date.today(), meeting[0].meetingTime) + timedelta(minutes=4, seconds=59)
                    lowerLate = datetime.combine(date.today(), meeting[0].meetingTime) + timedelta(minutes=5)
                    upperLate = datetime.combine(date.today(), meeting[0].meetingTime) + timedelta(hours=1, minutes=14,
                                                                                                   seconds=59)
                    absentTime = datetime.combine(date.today(), meeting[0].meetingTime) + timedelta(hours=1, minutes=15)
                    if currentTime <= tooEarly:
                        messages.info(request, "You are early, please come back during your meeting time. (Note: can "
                                               "enter 5 minutes early)")
                    elif lowerPresent <= currentTime <= upperPresent:
                        meeting[0].present.add(request.user)
                        meeting[0].not_applicable.remove(request.user)
                        isPresent = True
                        # messages.info(request, "You were marked as Present.")
                    elif lowerLate <= currentTime <= upperLate:
                        meeting[0].late.add(request.user)
                        meeting[0].not_applicable.remove(request.user)
                        isLate = True
                        # messages.info(request, "You were marked as Late.")
                    elif currentTime >= absentTime:
                        meeting[0].absent.add(request.user)
                        meeting[0].not_applicable.remove(request.user)
                        isAbsent = True
                        # messages.info(request, "You were marked as Absent.")

            elif request.GET.get("attendance_code") == '' and "attendance_code" in request.GET:
                messages.error(request, "Must input a code.")
            elif request.GET.get("attendance_code") != meeting[0].randomString and "attendance_code" in request.GET:
                messages.error(request, "The input did not meet the correct attendance code for the " + meeting[
                    0].meetingString + " meeting.")
        else:
            messages.error(request, "You are not enrolled in this class")

    else:
        found = False
    context = {"class": localCourse,
               "found": found,
               "TodayDate": todayDate,
               "present": isPresent,
               "late": isLate,
               "absent": isAbsent
               }
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
            currentDate = date.today()
            currentDateTime = datetime.now()
            recentMeeting = Meeting_Day.objects.filter(course=localCourse, meetingDate=currentDate)
            if recentMeeting and localCourse.lastScanned <= currentDate:
                absentDateTime = datetime.combine(date.today(), recentMeeting[0].meetingTime) + timedelta(hours=1,
                                                                                                      minutes=15)
                if recentMeeting and currentDateTime > absentDateTime:
                    rangeOfMeetings = Meeting_Day.objects.filter(
                        meetingDate__range=[localCourse.lastScanned, currentDate])
                    for meeting_day in rangeOfMeetings:
                        migrate_absentees = meeting_day.not_applicable.all()
                        for student in migrate_absentees:
                            meeting_day.absent.add(student)
                            meeting_day.not_applicable.remove(student)
                elif recentMeeting and not currentDateTime > absentDateTime and localCourse.lastScanned < (
                        currentDate + timedelta(days=-1)):
                    rangeOfMeetings = Meeting_Day.objects.filter(
                        meetingDate__range=[localCourse.lastScanned, currentDate + timedelta(days=-1)])
                    for meeting_day in rangeOfMeetings:
                        migrate_absentees = meeting_day.not_applicable.all()
                        for student in migrate_absentees:
                            meeting_day.absent.add(student)
                            meeting_day.not_applicable.remove(student)
            elif localCourse.lastScanned < currentDate:
                rangeOfMeetings = Meeting_Day.objects.filter(
                    meetingDate__range=[localCourse.lastScanned, currentDate])
                for meeting_day in rangeOfMeetings:
                    migrate_absentees = meeting_day.not_applicable.all()
                    for student in migrate_absentees:
                        meeting_day.absent.add(student)
                        meeting_day.not_applicable.remove(student)
            localCourse.lastScanned = currentDate
            localCourse.save()

            meeting = Meeting_Day.objects.filter(course=localCourse, meetingString=request.GET.get('meeting_dates'))
            print("meeting: ",meeting)
            print(request.GET.get('meeting_dates'))
            if meeting:
                meetingDay = meeting[0]
                randomString = meeting[0].randomString
                presentCount = len(meeting[0].present.all())
                lateCount = len(meeting[0].late.all())
                absentCount = len(meeting[0].absent.all())
                selectedOption = meeting[0].meetingString
            else:
                meetingDay =  all_meeting_days[0]
                randomString = all_meeting_days[0].randomString
                presentCount = len(all_meeting_days[0].present.all())
                lateCount = len(all_meeting_days[0].late.all())
                absentCount = len(all_meeting_days[0].absent.all())
                selectedOption = all_meeting_days[0].meetingString
            qrUrl = request._current_scheme_host+"/class/"+str(localCourse.id)+"/takeAttendance?attendance_code="+randomString
            context = {"class": localCourse,
                       "Meeting_Days": all_meeting_days,
                       "meeting_day": meetingDay,
                       "selected_option": selectedOption,
                       "present_count": presentCount,
                       "late_count": lateCount,
                       "absent_count": absentCount,
                       "random_string": randomString,
                       "qr_url": qrUrl
                       }
        else:
            template = loader.get_template('attendance/UpdateSettings.html')
            context = {}
    else:
        context = {}
        template = loader.get_template('attendance/permissionDenial.html')

    return HttpResponse(template.render(context, request))
