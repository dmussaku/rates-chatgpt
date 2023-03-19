from django.contrib import admin

# Register models in quotation app

from quotation.models import Quote, QuoteOption, QuoteLineItem

admin.site.register(Quote)
admin.site.register(QuoteOption)
admin.site.register(QuoteLineItem)
