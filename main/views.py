from dataclasses import dataclass
from enum import Enum
from typing import Literal
from urllib.parse import parse_qs

import django.db.models
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from main.models import Activity, Bank, PlaceType, Specialization, PriceData as Price


def get_payments(
        custom_payments=None,
        activities_price_total=None,
        activities_price_total_start_value=None,
        visa_quotas_price_total=None,
        visa_quotas_price_total_start_value=None,
        visa_now_price_total=None,
        visa_now_price_total_start_value=None,
        visa_now_services=None,
        visa_now_services_start_value=None,
        private_shareholders_price_total=None,
        private_shareholders_price_total_start_value=None,
        legal_shareholders_price_total=None,
        legal_shareholders_price_total_start_value=None,
        bank_account_registration_service=None,
        bank_account_registration_service_start_value=None,
        office_price_total=None,
        office_price_start_value=None,
        office_search_service=None,
        office_search_service_start_value=None,
        company_registration=None,
        company_registration_start_value=None,
        registration_service=None,
        registration_service_start_value=None
    ):

    payments = []

    if activities_price_total:
        payments.append(PriceDataView(
            description='Регистрация видов деятельности',
            value=activities_price_total,
            is_start_value=activities_price_total_start_value,
        ))
    if visa_quotas_price_total:
        payments.append(PriceDataView(
            description='Визовые квоты',
            value=visa_quotas_price_total,
            is_start_value=visa_quotas_price_total_start_value,
        ))
    if visa_now_price_total:
        payments.append(PriceDataView(
            description='Выпуск виз',
            value=visa_now_price_total,
            is_start_value=visa_now_price_total_start_value,
        ))
    if visa_now_services:
        payments.append(PriceDataView(
            description='Услуга по выпуску виз',
            value=visa_now_services,
            is_start_value=visa_now_services_start_value,
        ))
    if private_shareholders_price_total:
        payments.append(PriceDataView(
            description='Регистрация всех акционеров физ. лиц',
            value=private_shareholders_price_total,
            is_start_value=private_shareholders_price_total_start_value,
        ))
    if legal_shareholders_price_total:
        payments.append(PriceDataView(
            description='Регистрация всех акционеров юр. лиц',
            value=legal_shareholders_price_total,
            is_start_value=legal_shareholders_price_total_start_value,
        ))
    if bank_account_registration_service:
        payments.append(PriceDataView(
            description='Регистрация корпоративного счёта',
            value=bank_account_registration_service,
            is_start_value=bank_account_registration_service_start_value,
        ))
    if office_price_total:
        payments.append(PriceDataView(
            description='Аренда офиса',
            value=office_price_total,
            is_start_value=office_price_start_value,
        ))
    if office_search_service:
        payments.append(PriceDataView(
            description='Услуга по подбору офиса',
            value=office_search_service,
            is_start_value=office_search_service_start_value,
        ))

    if company_registration:
        payments.append(PriceDataView(
            description='Регистрация компании',
            value=company_registration,
            is_start_value=company_registration_start_value,
        ))

    if custom_payments:
        payments += custom_payments


    if registration_service:
        payments.append(PriceDataView(
            description='Профессиональные услуги',
            value=registration_service,
            is_start_value=registration_service_start_value,
        ))

    return payments


@dataclass
class ActivityData:
    activity: Activity
    specializations: list[Specialization]


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

        self.office: Literal['real', 'minimal', 'no'] = self.post.get('office')
        self.real_office_area = self.post.get('real_office_area')

        self.private_shareholders_count: int = int(self.post.get('private_shareholders_count', 0))
        self.legal_shareholders_count: int = int(self.post.get('legal_shareholders_count', 0))
        self.legal_shareholders_registrations: list[str] = self.body.get('legal_shareholders_registrations')
        self.shareholders_nationality: list[str] = self.body.get('shareholders_nationality')
        self.nominal_shareholder = self.post.get('nominal_shareholder')
        self.nominal_director = self.post.get('nominal_director')
        self.nominal_secretary = self.post.get('nominal_secretary')
        self.full_name: str = self.post.get('full_name')
        self.email: str = self.post.get('email')

        self.bank_account: Literal['company', 'personal', 'no'] = self.post.get('bank_account')
        self.contract_of_residence: Literal['self', 'minimal'] = self.post.get('contract_of_residence')

        self.banks: QuerySet = Bank.objects.filter(id__in=self.body.get('bank_names', []))
        self.bank_currency = self.post.get('bank_currency')
        self.bank_month_activity_input_min = self.post.get('bank_month_activity_input_min')
        self.bank_month_activity_input_max = self.post.get('bank_month_activity_input_max')
        self.bank_month_activity_output_min = self.post.get('bank_month_activity_output_min')
        self.bank_month_activity_output_max = self.post.get('bank_month_activity_output_max')

        self.bank_minimal_monthly_balance = self.post.get('bank_minimal_monthly_balance')

        self.bank_minimal_monthly_custom_balance = self.post.get('bank_minimal_monthly_custom_balance')
        self.bank_minimal_monthly_balance = self.bank_minimal_monthly_custom_balance

        self.source_of_funds = self.post.get('source_of_funds')

        self.company_annual_turnover_this_year = self.post.get('company_annual_turnover_this_year')
        self.company_annual_turnover_next_year = self.post.get('company_annual_turnover_next_year')
        self.company_annual_turnover_from_two_years = self.post.get('company_annual_turnover_from_two_years')

    def parse_activities(self):
        activities = []
        for activity_id in self.body.get('activities', []):
            activity = Activity.objects.get(id=activity_id)
            specializations = list(Specialization.objects.filter(id__in=self.body.get(f'specialization_{activity_id}',[])).all())
            activities.append(
                ActivityData(
                    activity=activity,
                    specializations=specializations,
                )
            )

        return activities



@dataclass
class PriceDataValueView:
    name: str
    value: str


class PriceDataView:

    def __init__(self,
                 description:str,
                 value = None,
                 values: list[PriceDataValueView] = None,
                 is_start_value: bool= False
                ) -> None:
        self.description=description
        self.value=value
        self.values=values
        self.is_start_value=is_start_value

        if values:
            self.value=sum([v.value for v in values])

class Payments:
    def __init__(self, payments: list[PriceDataView], cost_price_total):
        self.payments = payments
        self.is_start_value = any([p.is_start_value for p in payments])
        self.price_total = sum(p.value if p.value else float(p.total_value) for p in payments)
        self.cost_price_total = cost_price_total

@dataclass
class UnavailableOption:
    name: str


class Solution:
    def __init__(self, place_name: str, payments: list[Price], unavailable: list[UnavailableOption] = None) -> None:
        self.place_name = place_name
        self.payments = payments
        self.unavailable = [u for u in unavailable if u] if unavailable else None


class PriceData:

    def __init__(self, data: FormData):
        self.data = data

    def get_solutions(self):
        solutions = []
        other_payments = self.other_payments()

        if self.data.uae_business_area:
            if self.data.uae_business_full_area:
                solutions.append(self.mainland())
            else:
                solutions.append(self.mainland())
                solutions.append(self.ifza())
                solutions.append(self.uaq())
        else:
            solutions.append(self.offshore())
            solutions.append(self.mainland())
            solutions.append(self.ifza())
            solutions.append(self.uaq())

        for solution in solutions:
            solution.payments.payments += other_payments.payments.payments
            solution.payments.price_total += other_payments.payments.price_total

        return solutions


    def other_payments(self):
        """
        Payments that dont depend on the place of the company
        """
        payments = []

        if self.data.contract_of_residence == 'minimal':
            payments.append(
                PriceDataView(
                    description='Контракт на проживание',
                    values=[
                        PriceDataView(description='Tenancy contract', value=18300),
                        PriceDataView(description='DEWA Registration', value=2200),
                    ]
            ))

        if any([self.data.nominal_shareholder,self.data.nominal_director, self.data.nominal_secretary]):
            value, description = self.calculate_nominal_service()

            payments.append(
                PriceDataView(
                    description=description,
                    value=value,
                ))

        return Solution(
            place_name='Другие платежи',
            payments=Payments(
                payments=payments,
                cost_price_total=None
            ),
        )

    def offshore(self) -> Solution:
        activities_price_total, activities_cost_price_total = self.calculate_specializations(free_count=3, price=1000)
        bank_account_registration_service = self.calculate_bank_account_registration_service()

        # shareholder private
        private_shareholders_count = self.data.private_shareholders_count
        free_private_shareholders_count = 3
        private_shareholder_price = 275

        private_shareholders_price_total = 0
        if private_shareholders_count > free_private_shareholders_count:
            private_shareholders_price_total = (private_shareholders_count - free_private_shareholders_count) * private_shareholder_price
        private_shareholders_cost_price_total = private_shareholders_price_total


        # shareholder legal
        legal_shareholders_count = self.data.legal_shareholders_count
        free_legal_shareholders_count = 3
        legal_shareholder_price = 275

        legal_shareholders_price_total = 0
        if legal_shareholders_count > free_legal_shareholders_count:
            legal_shareholders_price_total = (legal_shareholders_count - free_legal_shareholders_count) * legal_shareholder_price
        legal_shareholders_cost_price_total = legal_shareholders_price_total

        company_registration = 3000 * 1.05
        registration_service = 6500

        cost_price_total = sum([
            activities_cost_price_total,
            private_shareholders_cost_price_total,
            legal_shareholders_cost_price_total,
            company_registration,
        ])
        price_total = sum([
            activities_price_total,
            bank_account_registration_service,
            private_shareholders_price_total,
            legal_shareholders_price_total,
            company_registration,
            registration_service,
        ])
        payments = get_payments(
            activities_price_total=activities_price_total,
            bank_account_registration_service=bank_account_registration_service,
            private_shareholders_price_total=private_shareholders_price_total,
            legal_shareholders_price_total=legal_shareholders_price_total,
            company_registration=company_registration,
            registration_service=registration_service,
        )

        unavailable = [
            UnavailableOption(name='Выпуск виз') if self.data.visa_quotas or self.data.visa_quotas_now else None,
        ]

        payments_data = Payments(
            payments=payments,
            cost_price_total=cost_price_total,
        )


        return Solution(
            place_name='Оффшорная компания',
            payments=payments_data,
            unavailable=unavailable,
        )

    def mainland(self) -> Solution:
        activities_count = len(self.data.activities)
        specializations_count = len(sum([a.specializations for a in self.data.activities], []))
        free_specializations_count = 10
        activity_cost_price = 20000
        activities_price_total = activity_cost_price

        need_companies = False
        if activities_count > 1:
            need_companies = True # TODO calculate other companies

        if specializations_count > free_specializations_count:
            pass # TODO think about it

        bank_account_registration_service = self.calculate_bank_account_registration_service()

        # visa now
        visa_cost_price = 5200 * 1.05
        visa_professional_services = 5500
        visa_now_cost_price_total = visa_cost_price * self.data.visa_quotas_now
        visa_now_price_total = visa_cost_price * self.data.visa_quotas_now
        visa_now_services = visa_professional_services * self.data.visa_quotas_now

        office_cost_price = 0
        office_price_total = 0
        office_search_service = 0
        office_price_start_value = False
        if self.data.office == 'real':
            office_cost_price = 25000
            office_price_total = office_cost_price
            office_price_start_value = True
            office_search_service = 4000

        elif self.data.office == 'minimal':
            office_cost_price = 10000
            office_price_total = office_cost_price
            office_search_service = 0

        # professional services
        registration_service = 8000

        cost_price_total = sum([
            activity_cost_price,
            visa_now_cost_price_total,
            office_cost_price,

        ])
        price_total = sum([
            activities_price_total,
            visa_now_price_total,
            visa_now_services,
            office_price_total,
            office_search_service,
            bank_account_registration_service,
            registration_service,
        ])
        payments = get_payments(
            activities_price_total=activities_price_total,
            activities_price_total_start_value=True,
            visa_now_price_total=visa_now_price_total,
            visa_now_price_total_start_value=True,
            visa_now_services=visa_now_services,
            office_price_total=office_price_total,
            office_price_start_value=office_price_start_value,
            office_search_service=office_search_service,
            bank_account_registration_service=bank_account_registration_service,
            registration_service=registration_service,
        )

        unavailable = [
            UnavailableOption(name='Несколько видов деятельности') if activities_count > 1 else None,
        ]


        payments_data = Payments(
            payments=payments,
            cost_price_total=cost_price_total,
        )
        return Solution(
            place_name='Мейнленд',
            payments=payments_data,
            unavailable=unavailable,
        )

    def ifza(self) -> Solution:
        activities_price_total, activities_cost_price_total = self.calculate_specializations(free_count=3, price=1000)
        bank_account_registration_service = self.calculate_bank_account_registration_service()


        # visa quotas
        establishment_card_cost_price = 2000
        establishment_card_price_total = establishment_card_cost_price

        quotas_count = self.data.visa_quotas
        quotas_data = {
            0: {'price': 12900, 'cost_price': 10300},
            1: {'price': 14900, 'cost_price': 11900},
            2: {'price': 16900, 'cost_price': 13500},
            3: {'price': 18900, 'cost_price': 15100},
            4: {'price': 20900, 'cost_price': 16700},
        }
        max_key = max(quotas_data.keys())
        if quotas_count > max_key:
            quotas_count = max_key

        visa_quotas_price_total = quotas_data[quotas_count]['price'] +  establishment_card_price_total
        visa_quotas_cost_price_total = quotas_data[quotas_count]['cost_price'] + establishment_card_cost_price


        # visa now
        visa_professional_services = 4750
        residence_visa_fee = 3750
        residence_id_price = 500
        residence_medial_price = 500

        visa_now_cost_price_total = (residence_visa_fee + residence_id_price + residence_medial_price) * self.data.visa_quotas_now
        visa_now_price_total = visa_now_cost_price_total
        visa_now_services = visa_professional_services * self.data.visa_quotas_now

        # private_shareholder
        free_private_shareholder_count = 3
        private_shareholder_price = 350

        private_shareholders_price_total = 0
        if self.data.private_shareholders_count > free_private_shareholder_count:
            private_shareholders_price_total = (self.data.private_shareholders_count - free_private_shareholder_count) * private_shareholder_price
        private_shareholder_cost_price_total = private_shareholders_price_total


        # legal_shareholder
        legal_shareholder_price = 2000
        legal_shareholders_price_total = legal_shareholder_price * self.data.legal_shareholders_count
        legal_shareholders_cost_price_total = legal_shareholders_price_total


        office_cost_price = 0
        office_price_total = 0
        office_search_service = 0
        office_price_start_value = False

        if self.data.office == 'real':
            office_cost_price = 25000
            office_price_total = office_cost_price
            office_price_start_value = True
            office_search_service = 3000

        elif self.data.office == 'minimal':
            office_cost_price = 13900
            office_price_total = office_cost_price
            office_search_service = 0


        # professional services
        registration_service = 6600




        cost_price_total = sum([
            activities_cost_price_total,
            visa_quotas_cost_price_total,
            visa_now_cost_price_total,
            private_shareholder_cost_price_total,
            legal_shareholders_cost_price_total,
            office_cost_price,
            establishment_card_cost_price,
        ])
        price_total = sum([
            activities_price_total,
            visa_quotas_price_total,
            visa_now_price_total,
            private_shareholders_price_total,
            legal_shareholders_price_total,
            office_price_total,
            visa_now_services,
            bank_account_registration_service,
            office_search_service,
            registration_service,
            establishment_card_price_total,
        ])

        payments = get_payments(
            activities_price_total=activities_price_total,
            visa_quotas_price_total=visa_quotas_price_total,
            visa_now_price_total=visa_now_price_total,
            visa_now_services=visa_now_services,
            private_shareholders_price_total=private_shareholders_price_total,
            legal_shareholders_price_total=legal_shareholders_price_total,
            bank_account_registration_service=bank_account_registration_service,
            office_price_total=office_price_total,
            office_price_start_value=office_price_start_value,
            office_search_service=office_search_service,
            registration_service=registration_service,
        )
        unavailable = []

        payments_data = Payments(
            payments=payments,
            cost_price_total=cost_price_total,
        )
        return Solution(
            place_name='IFZA',
            payments=payments_data,
            unavailable=unavailable,
        )

    def uaq(self) -> Solution:
        place_type = PlaceType.objects.get(name='UAQ')
        custom_payments = []

        specialization_price = Price.objects.get(name='specialization', place_type=place_type)
        activities_price_total, activities_cost_price_total = self.calculate_specializations(free_count=specialization_price.has_free_amount, price=specialization_price.value)
        bank_account_registration_service = self.calculate_bank_account_registration_service()

        visa_now_price_total = 0
        visa_now_cost_price_total = 0
        visa_now_services = 0

        if self.data.visa_quotas == 1 and (self.data.office == 'no' or not self.data.office) and (self.data.bank_account == 'no' or not self.data.bank_account):
            package_1 = Price.objects.get_package_with_children(pk=1)
            custom_payments.append(package_1)

        else:
            package_2 = Price.objects.get_package_with_children(pk=7)
            custom_payments.append(package_2)

            if self.data.visa_quotas_now:
                visa_charge = Price.objects.get_package_with_children(pk=13)

                visa_now_professional_services = Price.objects.get(name='visa_now_professional_services', place_type=place_type)
                visa_now_fee_percentage = Price.objects.get(name='visa_now_fee_percentage', place_type=place_type)
                visa_now_price_total = (float(visa_charge.get_total_value()) * self.data.visa_quotas_now) * (1 + visa_now_fee_percentage.value/100)
                visa_now_services = (visa_now_professional_services.value * self.data.visa_quotas_now) * (1 + visa_now_fee_percentage.value/100)


        private_shareholders_price_total = 0 # TODO
        max_private_shareholders_count = Price.objects.get(name='max_private_shareholders_count', place_type=place_type)
        if self.data.private_shareholders_count > max_private_shareholders_count.value:
            return None

        # legal_shareholder
        legal_shareholder_price = Price.objects.get(name='legal_shareholder', place_type=place_type)
        legal_shareholders_price_total = legal_shareholder_price.value * self.data.legal_shareholders_count
        legal_shareholders_price_total_start_value = True


        # professional services
        registration_service = Price.objects.get(name='registration_service', place_type=place_type)

        cost_price_total = sum([
            activities_cost_price_total,
            visa_now_cost_price_total,
        ])

        payments = get_payments(custom_payments=custom_payments,
            activities_price_total=activities_price_total,
            visa_now_price_total=visa_now_price_total,
            visa_now_services=visa_now_services,
            bank_account_registration_service=bank_account_registration_service,
            private_shareholders_price_total=private_shareholders_price_total,
            legal_shareholders_price_total=legal_shareholders_price_total,
            legal_shareholders_price_total_start_value=legal_shareholders_price_total_start_value,
            registration_service=registration_service.value,
        )
        payments_data = Payments(
            payments=payments,
            cost_price_total=cost_price_total,
        )
        unavailable = []
        return Solution(
            place_name=place_type.name,
            payments=payments_data,
            unavailable=unavailable,
        )


    def calculate_specializations(self, free_count, price):
        specializations_count = len(sum([a.specializations for a in self.data.activities], []))

        price_total = 0
        if specializations_count > free_count:
            price_total = (specializations_count - free_count) * price
        cost_price_total = price_total

        return price_total, cost_price_total

    def calculate_bank_account_registration_service(self) -> int:
        bank_account_registration_service = 0
        if self.data.bank_account == 'company':
            bank_account_registration_service = 18500  # 5000 usd

        return bank_account_registration_service

    def calculate_nominal_service(self) -> (int, str):
        shareholder = self.data.nominal_shareholder
        director = self.data.nominal_director
        secretary = self.data.nominal_secretary

        if shareholder and director and secretary:
            return 9182.5, 'Номинальный сервис (акционер, директор, секретарь)'

        if secretary and (shareholder or director):
            if shareholder and director:
                return 9182.50, 'Номинальный сервис (акционер, директор, секретарь)'
            return 5509.5, f'Номинальный сервис (секретарь, {"акционер" if shareholder else "директор"})'

        if shareholder and director:
            return 7346, 'Номинальный сервис (акционер, директор)'

        cost = 0
        description = 'Номинальный сервис '
        if shareholder:
            cost += 4407.6
            description += '(акционер) '
        if director:
            cost += 4407.6
            description += '(директор) '
        if secretary:
            cost += 1836.50
            description += '(секретарь) '

        return cost, description.strip()


def index(request: WSGIRequest) -> HttpResponse:
    return render(request, 'main/index.html')

def get_solutions(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        data = FormData(request)
        price_data = PriceData(data)
        solutions = price_data.get_solutions()
        return render(request, 'main/solutions.html', context={'solutions': solutions})

@require_POST
def get_form(request: WSGIRequest) -> HttpResponse:
    context = {}
    match request.GET.get('part'):
        case 'activities':
            template_name = 'main/activities/index.html'
            context['activities'] = Activity.objects.all()

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

        case 'banks_name_list':
            template_name = 'main/bank_account_form/bank_name/list.html'
            context['bank_names'] = Bank.objects.all()


        case _:
            return HttpResponse('soon')


    return render(request, template_name, context)




def get_activity_detail(request: WSGIRequest) -> HttpResponse:

    context = {
        'activity': Activity.objects.get(id=request.GET.get('activity'))
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