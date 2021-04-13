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
    template = loader.get_template('enrolled_classes/enrolledClasses.html')
    all_classes = request.user.profile.course.all

    context = {
        "all_classes": all_classes
    }

    return HttpResponse(template.render(context, request))


# Checks if the input for add class is valid
def isInputValid(sectionNum, courseCode):
    sectionIsValid = False
    validCode = False
    validNum = False
    validCodes = {"COMM": 1, "CS": 1, "ECS": 1, "RHET": 1, "SE": 1}
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
        courseCode = request.POST["Course"]

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
                    new_class = Enrolled_Class.objects.create(sectionNumber=sectionNum, courseName=courseName, courseNumber=courseCode)
                new_class.save()
                profile.course.add(new_class)


            return redirect("/class")

        else:
            messages.error(request, "Please input a valid course code")

    context = {"error": None}
    return HttpResponse(template.render(context, request))

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