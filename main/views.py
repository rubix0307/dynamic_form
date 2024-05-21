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

        case 'registration_preferences_detail':
            template_name = 'main/form_blocks/inc/registration_preferences_detail.html'

        case 'outsource':
            template_name = 'main/freezone/block_5/index.html'

        case _:
            return HttpResponse('soon')


    return render(request, template_name, context)



@require_GET
def search_activity(request):
    query = request.GET.get('search_activity', '')
    activities_list = [(activity, activities[activity]['name']) for activity in activities.keys()]
    return render(request, 'main/form_blocks/inc/activities_list.html', {'activities': activities_list})

def get_activity_detail(request: WSGIRequest) -> HttpResponse:

    context = {
        'activity': activities.get(request.GET.get('activity')),
    }

    return render(request, 'main/form_blocks/inc/activity_detail.html', context)

def get_free_economic_zones_by_emirate_name(request: WSGIRequest) -> HttpResponse:
    economic_zones = {
        'dubai': [
            {'name':'Dubai Maritime City'},
            {'name':'Dubai Commercity'},
            {'name':'Dubai South'},
            {'name':'Dubai World Trade Centre'},
            {'name':'Dubai Design District'},
            {'name':'Dubai Science Park'},
            {'name':'International Humanitarian City'},
            {'name':'Dubai Multi Commodities Centre'},
            {'name':'Dubai Outsource City'},
            {'name':'Dubai Silicon Oasis'},
            {'name':'Dubai International Financial Centre'},
            {'name':'Dubai Internet City'},
            {'name':'Meydan Free Zone'},
            {'name':'Dubai Healthcare City'},
            {'name':'Dubai International Academic City'},
            {'name':'Dubai Production City'},
            {'name':'Dubai Studio City'},
            {'name':'Dubai Media City'},
            {'name':'DAFZ INDUSTRIAL PARK'},
            {'name':'Dubai Financial Services Authority (DFSA)'},
            {'name':'Gold & Diamond Park'},
            {'name':'DUBAI AIRPORT FREEZONE'},
            {'name':'Dubai Knowledge Park'},
            {'name':'Dubai Auto Zone (DAZ)'},
            {'name':'Jebel Ali Free Zone'},
            {'name':'Expo City Dubai'},
        ],
        'sharjah': [
            {'name':'sharjah test'},
            {'name':'sharjah test'},
            {'name':'sharjah test'},
            {'name':'sharjah test'},

        ],

    }
    emirate_name = request.GET.get('emirate_name', '').lower()
    context = {
        'emirate_name': emirate_name,
        'economic_zones': economic_zones.get(emirate_name),
    }

    return render(request, 'main/form_blocks/inc/emirate_economic_zone_detail.html', context)