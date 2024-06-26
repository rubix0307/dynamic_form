from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from main.models import PriceData

class PriceDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'price', 'cost_price', 'description', 'parent_link', 'place_type', 'has_free_quantity', 'extra_fee_link')
    list_filter = ('place_type', 'parent',)
    search_fields = ('name', 'description', 'price', 'cost_price', 'parent__id', 'parent__description', 'parent__price', 'parent__cost_price')

    def parent_link(self, obj):
        if obj.parent is not None:
            link = reverse("admin:main_pricedata_change", args=[obj.parent.id])
            return format_html('<a href="{}">{}</a>', link, obj.parent.name)
        return '-'
    parent_link.short_description = 'Parent'

    def extra_fee_link(self, obj):
        if obj.extra_fee is not None:
            return format_html('{} %',obj.extra_fee)
        return '-'
    extra_fee_link.short_description = 'Extra fee'

admin.site.register(PriceData, PriceDataAdmin)
