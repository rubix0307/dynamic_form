from dataclasses import dataclass
from enum import Enum
from typing import Literal
from urllib.parse import parse_qs

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
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

@dataclass
class Activity:
    name: str
    specializations: list[str]


def str_as_bool(value:str) -> bool:
    if value and value.isdigit():
        return bool(int(value))
    return False

def str_as_int(value:str) -> int:
    if value and value.isdigit():
        return int(value)
    return None


class FormData:

    def __init__(self, request):
        self.post = request.POST
        self.body = {k.decode('utf-8'): [v.decode('utf-8') for v in vs] for k, vs in parse_qs(request.body).items()}

        self.request = request
        self.uae_business_area: bool = str_as_bool(self.post.get('uae_business_area'))
        self.uae_business_full_area: bool = str_as_bool(self.post.get('uae_business_full_area'))

        self.activities = self.parse_activities()

        self.has_home_company: bool = str_as_bool(self.post.get('has_home_company'))
        self.home_company_activity: str = self.body.get('home_company_activity')
        self.home_company_activity_markets: list[str] = self.body.get('home_company_activity_market')
        self.home_company_website: str = self.post.get('is_home_company_website')

        self.is_resident = str_as_bool(self.post.get('is_resident'))
        self.visa_required = str_as_bool(self.post.get('visa_required'))
        self.visa_quotas: int = int(self.post.get('visa_quotas', 0))
        self.visa_quotas_now: int = int(self.post.get('visa_quotas_now', 0))


        self.private_shareholders_count: int = int(self.post.get('private_shareholders_count'))
        self.legal_shareholders_count: int = int(self.post.get('legal_shareholders_count'))
        self.legal_shareholders_registrations: list[str] = self.body.get('legal_shareholders_registrations')
        self.shareholders_nationality: list[str] = self.body.get('shareholders_nationality')

        self.full_name: str = self.post.get('full_name')
        self.email: str = self.post.get('email')

        self.bank_account: Literal['company', 'personal', 'no'] = self.post.get('bank_account')
        if self.bank_account == 'company':
            self.bank_name = self.post.get('bank_name')
            self.bank_currency = self.post.get('bank_currency')
            self.bank_month_activity_input_min = self.post.get('bank_month_activity_input_min')
            self.bank_month_activity_input_max = self.post.get('bank_month_activity_input_max')
            self.bank_month_activity_output_min = self.post.get('bank_month_activity_output_min')
            self.bank_month_activity_output_max = self.post.get('bank_month_activity_output_max')

            self.bank_minimal_monthly_balance = self.post.get('bank_minimal_monthly_balance')
            if self.bank_minimal_monthly_balance == 'custom':
                self.bank_minimal_monthly_custom_balance = self.post.get('bank_minimal_monthly_custom_balance')
                self.bank_minimal_monthly_balance = self.bank_minimal_monthly_custom_balance

            self.source_of_funds = self.post.get('source_of_funds')

            self.company_annual_turnover_this_year = self.post.get('company_annual_turnover_this_year')
            self.company_annual_turnover_next_year = self.post.get('company_annual_turnover_next_year')
            self.company_annual_turnover_from_two_years = self.post.get('company_annual_turnover_from_two_years')

    def parse_activities(self):
        return [Activity(name=activity_name,specializations=self.body.get(f'specialization_{activity_name}')) for activity_name in self.body.get('activities', [])]



def index(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        data = FormData(request)
    return render(request, 'main/index.html')

@require_POST
def get_form(request: WSGIRequest) -> HttpResponse:
    context = {}
    match request.GET.get('part'):
        case 'activities':
            template_name = 'main/activities/index.html'
            context['activities'] = [(activity, activities[activity]['name']) for activity in activities.keys()]

        case 'shareholder_question':
            template_name = 'main/shareholder_home/index.html'

        case 'shareholder_home_detail':
            template_name = 'main/shareholder_home/detail.html'

        case 'registration_preferences':
            template_name = 'main/preferences/index.html'

        case 'registration_preferences_detail':
            template_name = 'main/preferences/detail.html'

        case 'outsource':
            template_name = 'main/outsource/index.html'

        case 'visa':
            template_name = 'main/visa/index.html'

        case 'visa_detail':
            template_name = 'main/visa/detail.html'

        case 'shareholders':
            template_name = 'main/shareholders/index.html'

        case 'office_and_bank':
            template_name = 'main/office_and_bank/index.html'

        case 'office':
            template_name = 'main/office_and_bank/detail.html'

        case 'customer_data':
            template_name = 'main/customer_data/index.html'

        case 'uae_business_area_detail':
            template_name = 'main/uae_business_area/detail.html'

        case 'bank_account':
            template_name = 'main/bank_account_form/index.html'


        case _:
            return HttpResponse('soon')


    return render(request, template_name, context)



@require_GET
def search_activity(request):
    query = request.GET.get('search_activity', '')
    activities_list = [(activity, activities[activity]['name']) for activity in activities.keys()]
    return render(request, 'main/activities/list.html', {'activities': activities_list})

def get_activity_detail(request: WSGIRequest) -> HttpResponse:

    context = {
        'activity': activities.get(request.GET.get('activity')),
    }

    return render(request, 'main/activities/detail.html', context)

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

    return render(request, 'main/preferences/zone_detail.html', context)