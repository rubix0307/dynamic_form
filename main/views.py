from urllib.parse import parse_qs

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST


activities = {
    'construction': {
        'id':'construction',
        'name':'Construction',
        'specializations': [
            {'name':'Demolition and site preparation'},
            {'name':'Electrical, plumbing and other construction installation activities'},
            {'name':'Building completion and finishing'},
            {'name':'Other specialized construction activities'},
        ]
    },
    'wholesale_and_retail_trade_repair_of_motor_vehicles_and_motorcycles': {
        'id':'wholesale_and_retail_trade_repair_of_motor_vehicles_and_motorcycles',
        'name':'Wholesale and retail trade; repair of motor vehicles and motorcycles',
        'specializations': [
            {'name':'Retail sale of information and communications equipment in specialized stores'},
            {'name':'Retail sale of cultural and recreation goods in specialized stores'},
            {'name':'Retail sale of other goods in specialized stores'},
        ]
    },
}


def index(request: WSGIRequest) -> HttpResponse:

    data = {k.decode('utf-8'): [v.decode('utf-8') for v in vs] for k, vs in parse_qs(request.body).items()}
    return render(request, 'main/index.html')

@require_POST
def get_form(request: WSGIRequest) -> HttpResponse:
    context = {}
    match request.GET.get('part'):
        case 'activities':
            template_name = 'main/freezone/activities.html'
            context['activities'] = [(activity, activities[activity]['name']) for activity in activities.keys()]

        case 'shareholder_question':
            template_name = 'main/freezone/shareholder_home_company_questions.html'

        case 'registration_preferences':
            template_name = 'main/freezone/registration_preferences.html'

        case _:
            return HttpResponse('soon')


    return render(request, template_name, context)



@require_GET
def search_activity(request):
    query = request.GET.get('search_activity', '')
    activities_list = [(activity, activities[activity]['name']) for activity in activities.keys()]
    return render(request, 'main/form_blocks/inc/activities_list.html', {'activities': activities_list})

def get_activity_detail(request: WSGIRequest) -> HttpResponse:
    activity = activities.get(request.GET.get('activity'))


    context = {
        'activity': activity,
    }

    return render(request, 'main/form_blocks/inc/activity_detail.html', context)