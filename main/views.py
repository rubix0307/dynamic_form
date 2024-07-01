from dataclasses import dataclass
from typing import Literal
from urllib.parse import parse_qs

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Max, QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from main.models import Activity, Bank, PlaceType, Specialization, PriceData as Price


def get_payments(
        office: Price =None,
        office_search_service: Price =None,
        professional_service: Price =None,
        custom_payments=None,

        specialization_price=None,
        specialization_start_price=None,
        visa_quotas_price=None,
        visa_quotas_start_price=None,
        visa_now_price=None,
        visa_now_start_price=None,
        visa_now_services_price=None,
        visa_now_services_start_value=None,
        private_shareholders_price=None,
        private_shareholders_start_price=None,
        legal_shareholders_price=None,
        legal_shareholders_start_price=None,
        bank_account_registration_service_price=None,
        bank_account_registration_service_start_price=None,
        company_registration_price=None,
        company_registration_start_price=None,

    ):

    payments = []

    if specialization_price:
        payments.append(PriceDataView(
            name='Регистрация специализаций',
            value=specialization_price,
            is_start_value=specialization_start_price,
        ))


    if any([visa_quotas_price, visa_now_price, visa_now_services_price]):
        visa_payments = []
        if visa_quotas_price:
            visa_payments.append(PriceDataView(
                name='Визовые квоты',
                value=visa_quotas_price,
                is_start_value=visa_quotas_start_price,
            ))
        if visa_now_price:
            visa_payments.append(PriceDataView(
                name='Выпуск виз',
                value=visa_now_price,
                is_start_value=visa_now_start_price,
            ))
        if visa_now_services_price:
            visa_payments.append(PriceDataView(
                name='Услуга по выпуску виз',
                value=visa_now_services_price,
                is_start_value=visa_now_services_start_value,
            ))

        payments.append(
            PriceDataView(
                name='Визы',
                values=visa_payments,
            )
        )
    if private_shareholders_price:
        payments.append(PriceDataView(
            name='Регистрация всех акционеров физ. лиц',
            value=private_shareholders_price,
            is_start_value=private_shareholders_start_price,
        ))
    if legal_shareholders_price:
        payments.append(PriceDataView(
            name='Регистрация всех акционеров юр. лиц',
            value=legal_shareholders_price,
            is_start_value=legal_shareholders_start_price,
        ))
    if bank_account_registration_service_price:
        payments.append(PriceDataView(
            name='Регистрация корпоративного счёта',
            value=bank_account_registration_service_price,
            is_start_value=bank_account_registration_service_start_price,
        ))
    if office:
        payments.append(PriceDataView(
            name='Аренда офиса',
            value=office.price,
            is_start_value=office.is_start_value,
        ))
    if office_search_service:
        payments.append(PriceDataView(
            name='Услуга по подбору офиса',
            value=office_search_service.price,
            is_start_value=office_search_service.is_start_value,
        ))

    if company_registration_price:
        payments.append(PriceDataView(
            name='Регистрация компании',
            value=company_registration_price,
            is_start_value=company_registration_start_price,
        ))

    if custom_payments:
        payments += custom_payments


    if professional_service:
        payments.append(PriceDataView(
            name='Профессиональные услуги',
            value=professional_service.price,
            is_start_value=professional_service.is_start_value,
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
                 name:str,
                 value = None,
                 values: list[PriceDataValueView]|QuerySet = None,
                 is_start_value: bool= False
                ) -> None:
        self.name=name
        self.value=value
        self.values=values
        self.is_start_value=is_start_value

        if values:

            if type(values) is QuerySet:
                self.normalize_values(values)

            self.value=sum([v.value or 0 if 'value' in v.__dir__() else v.price or 0 for v in self.values])
            self.is_start_value = any([v.is_start_value for v in self.values]+[is_start_value])


    def normalize_values(self, values):
        new_values = []
        for value in values:

            new_values.append(PriceDataView(
                name=value.name,
                value=value.price,
                values=self.normalize_values(value.values_list),
                is_start_value=value.is_start_value,
            ))

        self.values = new_values
        self.is_start_value = any(v.is_start_value for v in self.values)
        return new_values

class Payments:
    def __init__(self, payments: list[PriceDataView], cost_price_total=None):
        self.payments = payments
        self.is_start_value = any([p.is_start_value for p in payments])
        self.price_total = sum(float(p.value) for p in payments)
        self.cost_price_total = cost_price_total

@dataclass
class UnavailableOption:
    name: str


class Solution:
    def __init__(self, place_type: str, payments: list[Price]) -> None:
        self.place_type: PlaceType = place_type
        self.payments = payments


class PriceData:

    def __init__(self, data: FormData):
        self.data = data

    def get_solutions(self):
        solutions = []
        other_payments = self.other_payments()

        # if self.data.uae_business_area:
        #     if self.data.uae_business_full_area:
        #         solutions.append(self.mainland())
        #     else:
        #         solutions.append(self.mainland())
        #         solutions.append(self.ifza())
        #         solutions.append(self.uaq())
        # else:
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
                    name='Контракт на проживание',
                    values=[
                        PriceDataView(name='Tenancy contract', value=18300),
                        PriceDataView(name='DEWA Registration', value=2200),
                    ]
            ))

        if any([self.data.nominal_shareholder,self.data.nominal_director, self.data.nominal_secretary]):
            value, description = self.calculate_nominal_service()

            payments.append(
                PriceDataView(
                    name=description,
                    value=value,
                ))

        return Solution(
            place_type=PlaceType(name='Другие платежи'),
            payments=Payments(
                payments=payments,
                cost_price_total=None
            ),
        )

    def offshore(self) -> Solution:
        place_type = PlaceType.objects.get(name='Offshore')
        custom_payments = []

        specialization = Price.objects.get(name='specialization', place_type=place_type)
        specialization_price, specialization_cost_price = self.calculate_specializations(free_count=specialization.has_free_quantity, price=specialization.price)
        bank_account_registration_service_price = self.calculate_bank_account_registration_service()

        # private_shareholder TODO duplicate code
        private_shareholder = Price.objects.get(name='private_shareholder', place_type=place_type)
        private_shareholders_price = 0
        private_shareholder_cost_price = 0
        if self.data.private_shareholders_count > private_shareholder.has_free_quantity:
            private_shareholders_price = (self.data.private_shareholders_count - private_shareholder.has_free_quantity) * private_shareholder.price
            private_shareholder_cost_price = (self.data.private_shareholders_count - private_shareholder.has_free_quantity) * private_shareholder.cost_price

        # legal_shareholder
        legal_shareholder = Price.objects.get(name='legal_shareholder', place_type=place_type)
        legal_shareholders_price = 0
        legal_shareholders_cost_price = 0
        if self.data.legal_shareholders_count > legal_shareholder.has_free_quantity:
            legal_shareholders_price = (self.data.legal_shareholders_count - legal_shareholder.has_free_quantity) * legal_shareholder.price
            legal_shareholders_cost_price = (self.data.legal_shareholders_count - legal_shareholder.has_free_quantity) * legal_shareholder.cost_price

        company_registration = Price.objects.get(name='company_registration', place_type=place_type)
        professional_service = Price.objects.get(name='professional_service', place_type=place_type)

        payments = get_payments(
            specialization_price=specialization_price,
            bank_account_registration_service_price=bank_account_registration_service_price,
            private_shareholders_price=private_shareholders_price,
            legal_shareholders_price=legal_shareholders_price,
            company_registration_price=company_registration.price * (1 + (company_registration.extra_fee or 0)/100),
            professional_service=professional_service,
        )

        payments_data = Payments(
            payments=payments,
        )

        return Solution(
            place_type=place_type,
            payments=payments_data,
        )

    def mainland(self) -> Solution:
        place_type = PlaceType.objects.get(name='Mainland')

        activities_count = len(self.data.activities)
        specializations_count = len(sum([a.specializations for a in self.data.activities], []))

        specialization = Price.objects.get(name='specialization', place_type=place_type)
        specialization_price = specialization.price

        need_companies = False
        if activities_count > 1:
            need_companies = True # TODO calculate other companies

        if specializations_count > specialization.has_free_quantity or 0:
            pass # TODO think about it

        bank_account_registration_service_price = self.calculate_bank_account_registration_service()

        # visa now
        visa_issue = Price.objects.get(name='visa_issue', place_type=place_type)
        visa_professional_services = Price.objects.get(name='visa_professional_services', place_type=place_type)
        visa_now_services_price = visa_professional_services.price * self.data.visa_quotas_now
        visa_now_price = visa_issue.price * self.data.visa_quotas_now * (1 + (visa_issue.extra_fee or 0)/100)
        visa_now_cost_price_total = visa_issue.cost_price * self.data.visa_quotas_now * (1 + (visa_issue.extra_fee or 0)/100)

        office = None
        office_search_service = None
        if self.data.office == 'real': # TODO duplicate code
            office = Price.objects.get(name='office_real', place_type=place_type)
            office_search_service = Price.objects.get(parent=office,name='office_search_service')

        elif self.data.office == 'minimal':
            office = Price.objects.get(name='office_minimal', place_type=place_type)
            office_search_service = Price.objects.get(parent=office,name='office_search_service')

        # professional services
        professional_service = Price.objects.get(name='professional_service', place_type=place_type)

        payments = get_payments(
            visa_now_price=visa_now_price,
            visa_now_start_price=visa_issue.is_start_value,
            visa_now_services_price=visa_now_services_price,

            specialization_price=specialization_price,
            bank_account_registration_service_price=bank_account_registration_service_price,
            office=office,
            office_search_service=office_search_service,
            professional_service=professional_service,
        )

        payments_data = Payments(
            payments=payments,
        )
        return Solution(
            place_type=place_type,
            payments=payments_data,
        )

    def ifza(self) -> Solution:
        place_type = PlaceType.objects.get(name='IFZA')

        specialization = Price.objects.get(name='specialization', place_type=place_type)
        specialization_price, specialization_cost_price = self.calculate_specializations(free_count=specialization.has_free_quantity, price=specialization.price)
        bank_account_registration_service_price = self.calculate_bank_account_registration_service()

        # visa quotas
        establishment_card = Price.objects.get(name='establishment_card', place_type=place_type)

        quotas_count = self.data.visa_quotas
        quotas_data = Price.objects.get(name='quotas_data', place_type=place_type)
        max_quantity = Price.objects.filter(parent=quotas_data).aggregate(Max('quantity'))['quantity__max']

        if quotas_count > max_quantity:
            quotas_count = max_quantity

        quotas_price = Price.objects.get(parent=quotas_data, quantity=quotas_count)
        visa_quotas_price = quotas_price.price + establishment_card.price
        visa_quotas_cost_price = quotas_price.cost_price + establishment_card.cost_price

        # visa now
        visa_professional_services = Price.objects.get(name='visa_professional_services', place_type=place_type)
        residence_visa_fee = Price.objects.get(name='residence_visa_fee', place_type=place_type)
        residence_id = Price.objects.get(name='residence_id', place_type=place_type)
        residence_medial = Price.objects.get(name='residence_medial', place_type=place_type)

        visa_now_services_price = visa_professional_services.price * self.data.visa_quotas_now
        visa_now_price = (residence_visa_fee.price + residence_id.price + residence_medial.price) * self.data.visa_quotas_now
        visa_now_cost_price = (residence_visa_fee.cost_price + residence_id.cost_price + residence_medial.cost_price) * self.data.visa_quotas_now

        # private_shareholder
        private_shareholder = Price.objects.get(name='private_shareholder', place_type=place_type)
        private_shareholders_price = 0
        private_shareholder_cost_price = 0
        if self.data.private_shareholders_count > private_shareholder.has_free_quantity:
            private_shareholders_price = (self.data.private_shareholders_count - private_shareholder.has_free_quantity) * private_shareholder.price
            private_shareholder_cost_price = (self.data.private_shareholders_count - private_shareholder.has_free_quantity) * private_shareholder.cost_price

        # legal_shareholder
        legal_shareholder = Price.objects.get(name='legal_shareholder', place_type=place_type)
        legal_shareholders_price = 0
        legal_shareholders_cost_price = 0
        if self.data.legal_shareholders_count > legal_shareholder.has_free_quantity:
            legal_shareholders_price = (self.data.legal_shareholders_count - legal_shareholder.has_free_quantity) * legal_shareholder.price
            legal_shareholders_cost_price = (self.data.legal_shareholders_count - legal_shareholder.has_free_quantity) * legal_shareholder.cost_price


        office = Price()
        office_search_service = Price()

        if self.data.office == 'real':
            office = Price.objects.get(name='office_real', place_type=place_type)
            office_search_service = Price.objects.get(parent=office, name='office_search_service')

        elif self.data.office == 'minimal':
            office = Price.objects.get(name='office_minimal', place_type=place_type)
            office_search_service = Price.objects.get(parent=office,name='office_search_service')


        # professional services
        professional_service = Price.objects.get(name='registration_service', place_type=place_type)


        payments = get_payments(
            specialization_price=specialization_price,
            visa_quotas_price=visa_quotas_price,
            visa_now_price=visa_now_price,
            visa_now_services_price=visa_now_services_price,
            private_shareholders_price=private_shareholders_price,
            legal_shareholders_price=legal_shareholders_price,
            bank_account_registration_service_price=bank_account_registration_service_price,
            office=office,
            office_search_service=office_search_service,
            professional_service=professional_service,
        )

        payments_data = Payments(
            payments=payments,
        )
        return Solution(
            place_type=place_type,
            payments=payments_data,
        )

    def uaq(self) -> Solution:
        place_type = PlaceType.objects.get(name='UAQ')
        custom_payments = []

        specialization = Price.objects.get(name='specialization', place_type=place_type)
        specialization_price, specialization_cost_price = self.calculate_specializations(free_count=specialization.has_free_quantity, price=specialization.price)
        bank_account_registration_service_price = self.calculate_bank_account_registration_service()

        visa_now_price = 0
        visa_now_services_price = 0

        if self.data.visa_quotas == 1 and (self.data.office == 'no' or not self.data.office) and (self.data.bank_account == 'no' or not self.data.bank_account):
            package_1 = Price.objects.get_package_with_children(pk=1)

            custom_payments.append(PriceDataView(
                name=package_1.name,
                values=package_1.values_list,
                is_start_value=package_1.is_start_value,
            ))

        else:
            package_2 = Price.objects.get_package_with_children(pk=7)
            custom_payments.append(PriceDataView(
                name=package_2.name,
                values=package_2.values_list,
                is_start_value=package_2.is_start_value,
            ))

            if self.data.visa_quotas_now:
                visa_charge = Price.objects.get_package_with_children(name='Visa charges', place_type=place_type)
                visa_now_professional_services = Price.objects.get(name='visa_now_professional_services', place_type=place_type)

                visa_now_price = (visa_charge.get_total_price() * self.data.visa_quotas_now) * (1 + (visa_charge.extra_fee or 0)/100)
                visa_now_services_price = (visa_now_professional_services.price * self.data.visa_quotas_now) * (1 + (visa_charge.extra_fee or 0)/100)


        private_shareholders_price = 0 # TODO
        max_private_shareholders_count = Price.objects.get(name='max_private_shareholders_count', place_type=place_type)
        if self.data.private_shareholders_count > max_private_shareholders_count.quantity:
            return None

        # legal_shareholder
        legal_shareholder = Price.objects.get(name='legal_shareholder', place_type=place_type)
        legal_shareholders_price = legal_shareholder.price * self.data.legal_shareholders_count
        legal_shareholders_start_price = legal_shareholder.is_start_value

        # professional services
        registration_service = Price.objects.get(name='registration_service', place_type=place_type)

        payments = get_payments(
            custom_payments=custom_payments,
            specialization_price=specialization_price,
            visa_now_price=visa_now_price,
            visa_now_services_price=visa_now_services_price,
            bank_account_registration_service_price=bank_account_registration_service_price,
            private_shareholders_price=private_shareholders_price,
            legal_shareholders_price=legal_shareholders_price,
            legal_shareholders_start_price=legal_shareholders_start_price,
            professional_service=registration_service,
        )
        payments_data = Payments(
            payments=payments,
        )
        return Solution(
            place_type=place_type,
            payments=payments_data,
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
        return render(request, 'main/solutions/index.html', context={'solutions': solutions})

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