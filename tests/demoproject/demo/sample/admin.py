from django.contrib import admin

from demo.sample.models import DemoModel


@admin.register(DemoModel)
class DemoModelAdmin(admin.ModelAdmin):
    model = DemoModel
    list_filter = (
        'name',
    )
    list_display = (
        'name',
        'boolean_field',
    )
