from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register models in quotation app

from quotation.models import Quote, QuoteOption, QuoteLineItem


class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "original_input", "num_of_options", "quote_url")

    @admin.display
    def num_of_options(self, obj):
        return obj.options.count()
    
    @admin.display
    def quote_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>".format(url=reverse("quotation:quote", args=[obj.id])))


admin.site.register(Quote, QuoteAdmin)
admin.site.register(QuoteOption)
admin.site.register(QuoteLineItem)
