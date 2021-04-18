from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Enrolled_Class
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Create your views here.
@login_required(login_url='/login/')
def class_view(request):
    def_group = ""
    all_groups = request.user.groups.all()
    for group in all_groups:
        def_group = group.name

    template = loader.get_template('enrolled_classes/enrolledClasses.html')
    all_classes = request.user.profile.course.all

    context = {
        "all_classes": all_classes,
        "group": def_group
    }

    return HttpResponse(template.render(context, request))


# Checks if the input for add class is valid
def isInputValid(sectionNum, courseCode):
    sectionIsValid = False
    validCode = False
    validNum = False
    validCodes = {"ACCT": 1, "ACN": 1, "ACTS": 1, "AERO": 1, "AHST": 1, "AMS": 1, "ARAB": 1, "ARHM": 1, "ARTS": 1,
                  "ATCM": 1, "AUD": 1, "BA": 1, "BBSU": 1, "BCOM": 1, "BIOL": 1, "BIS": 1, "BLAW": 1, "BMEN": 1,
                  "BPS": 1, "BUAN": 1, "CE": 1, "CGS": 1, "CHEM": 1, "CHIN": 1, "CLDP": 1, "COMD": 1, "COMM": 1,
                  "CRIM": 1, "CRWT": 1, "CS": 1, "DANC": 1, "ECON": 1, "ECS": 1, "ECSC": 1, "ED": 1, "EE": 1, "EEBM": 1,
                  "EECS": 1, "EECT": 1, "EEDG": 1, "EEGR": 1, "EEMF": 1, "EEOP": 1, "EEPE": 1, "EERF": 1, "EESC": 1,
                  "ENGR": 1, "ENGY": 1, "ENTP": 1, "ENVR": 1, "EPCS": 1, "EPPS": 1, "FILM": 1, "FIN": 1, "FREN": 1,
                  "FTEC": 1, "GEOG": 1, "GEOS": 1, "GERM": 1, "GISC": 1, "GOVT": 1, "GST": 1, "HCS": 1, "HDCD": 1,
                  "HIST": 1, "HLTH": 1, "HMGT": 1, "HONS": 1, "HUAS": 1, "HUHI": 1, "HUMA": 1, "HUSL": 1, "IDEA": 1,
                  "IMS": 1, "IPEC": 1, "ISAE": 1, "ISAH": 1, "ISIS": 1, "ISNS": 1, "ITSS": 1, "JAPN": 1, "KORE": 1,
                  "LANG": 1, "LATS": 1, "LIT": 1, "MAIS": 1, "MAS": 1, "MATH": 1, "MECH": 1, "MECO": 1, "MILS": 1,
                  "MIS": 1, "MKT": 1, "MSEN": 1, "MTHE": 1, "MUSI": 1, "NATS": 1, "NSC": 1, "OB": 1, "OBHR": 1,
                  "OPRE": 1, "PA": 1, "PHIL": 1, "PHIN": 1, "PHYS": 1, "PPOL": 1, "PPPE": 1, "PSCI": 1, "PSY": 1,
                  "PSYC": 1, "REAL": 1, "RELS": 1, "RHET": 1, "RMIS": 1, "SCI": 1, "SE": 1, "SMED": 1, "SOC": 1,
                  "SPAN": 1, "SPAU": 1, "STAT": 1, "SYSE": 1, "SYSM": 1, "TE": 1, "THEA": 1, "UNIV": 1, "UTSW": 1,
                  "VPAS": 1}
    tempCode = ""
    tempNum = ""

    if (len(sectionNum) == 3):
        sectionIsValid = True
    for i in range(0, len(courseCode)):
        if courseCode[i].isalpha():
            courseCode[i]
            tempCode += courseCode[i]
        else:
            tempNum += courseCode[i]
    courseCode = tempCode + tempNum
    if len(tempNum) == 4:
        validNum = True
    try:
        if validCodes[tempCode]:
            validCode = True
    except KeyError:
        return False, courseCode

    if validCode == True and validNum == True and sectionIsValid == True:
        return True, courseCode
    return False, courseCode


@login_required(login_url='/login/')
def add_class_view(request):
    template = loader.get_template('enrolled_classes/addClass.html')
    found = False
    def_group = ""

    if request.method == "POST":
        courseName = request.POST["CourseName"]
        sectionNum = request.POST["Section"]
        courseCode = request.POST["prefix"] + request.POST["Course"]

        all_groups = request.user.groups.all()
        for group in all_groups:
            def_group = group.name

        courseCode.upper()
        valid, courseCode = isInputValid(sectionNum, courseCode)

        if valid:
            all_classes = Enrolled_Class.objects.all()
            profile = request.user.profile
            for course in all_classes:
                if course.sectionNumber == sectionNum and course.courseNumber == courseCode:
                    if def_group == "Professor":
                        course.professor = request.user
                        course.save()
                    profile.course.add(course)
                    found = True
                    break;

            if not found:
                if def_group == "Professor":
                    new_class = Enrolled_Class.objects.create(professor=request.user, sectionNumber=sectionNum, \
                                                              courseName=courseName, courseNumber=courseCode)
                else:
                    new_class = Enrolled_Class.objects.create(sectionNumber=sectionNum, courseName=courseName,
                                                              courseNumber=courseCode)
                new_class.save()
                profile.course.add(new_class)

            return redirect("/class")

        else:
            messages.error(request, "Please input a valid course code")

    context = {"error": None}
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def class_delete(request, pk):
    course = get_object_or_404(Enrolled_Class, pk=pk)

    if request.method == 'POST':
        def_group = ""
        all_groups = request.user.groups.all()
        for group in all_groups:
            def_group = group.name
        if def_group == "Professor":
            course.professor = None
            course.save()
        request.user.profile.course.remove(course)
        return redirect('/class')

    return render(request, 'enrolledClasses.html', {'class': Enrolled_Class})


@login_required(login_url='/login/')
def class_settings_view(request, pk):
    def_group = ""
    all_groups = request.user.groups.all()
    for group in all_groups:
        def_group = group.name
    if def_group == "Professor":
        template = loader.get_template('enrolled_classes/classSettings.html')
        course = Enrolled_Class.objects.get(id=pk)
        context = {"class": course}

        if request.method == 'POST':
            start = request.POST.get('start', False)
            end = request.POST.get('end', False)
            time = request.POST.get('time', False)
    else:
        context = {}
        template = loader.get_template('permissionDenial.html')

    return HttpResponse(template.render(context, request))
