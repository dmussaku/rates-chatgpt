from typing import Dict, List
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormView
from django.template import loader
import urllib.parse
from django.utils.http import urlencode
from rates.models import Port, MainRate, Surcharge, SurchargeTypes
from rates.clients import OpenAIClient
from rates.forms import ChatInputForm
from quotation.models import Quote, QuoteOption, QuoteLineItem


class ChatView(FormView):
    template_name = "chat.html"
    form_class = ChatInputForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        url = super().get_success_url()
        return f"{url}?{urlencode(kwargs)}"

    def run_gpt3(self, text: str) -> Dict:
        cli = OpenAIClient()
        return cli.get_answer(text)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        text: str = form.cleaned_data["text"]
        chat_response: Dict = self.run_gpt3(text)
        # chat_response example:
        # {
        #     "pol": {"name": "Shanghai", "code": "CNSHA", "country_code": "CN"}
        #     "pod": {"name": "Los Angeles", "code": "USLAX", "country_code": "US"}
        #     "containers": [{"type": "20gp", "amount": 2, "goods": "apples"}],
        #     "is_dangerous": True,
        #     "is_hazardous": False,
        #     "is_customs_needed": True,
        # }

        quote = Quote.objects.create_quote(
            text,
            chat_response,
        )
        return HttpResponseRedirect(
            reverse("quotation:quote", kwargs={"quote_id": quote.id})
        )
