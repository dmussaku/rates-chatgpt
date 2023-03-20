# create a TemplateView called QuoteView in quotation app

# app/quotation/views.py
import json

from django.views.generic import TemplateView
from quotation.models import Quote


class QuoteView(TemplateView):
    template_name = "quote.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quote_id = self.kwargs.get("quote_id")
        quote = Quote.objects.get(id=quote_id)
        context["quote"] = quote
        return context
