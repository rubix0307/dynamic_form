from django.contrib import admin

from main.models import PriceData


class PriceDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'description', 'parent', 'place_type', 'has_free_amount')
    list_filter = ('place_type', 'parent',)
    search_fields = ('description',)

admin.site.register(PriceData, PriceDataAdmin)