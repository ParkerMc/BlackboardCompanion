from django.http import HttpResponse
from django.template import loader


def attendance_professor(request):
    template = loader.get_template('attendance_professor.html')
    context = {}
    return HttpResponse(template.render(context, request))

