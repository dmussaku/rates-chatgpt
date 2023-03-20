# create a manager for Quote model in quotation app

# app/quotation/managers.py
from typing import Dict, List
from django.db import models

from rates.models import MainRate, Surcharge, SurchargeTypes, Port


class QuoteManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "options",
                "options__line_items",
            )
        )

    def create_quote(
        self,
        original_input: str,
        search_params: Dict,
    ):
        quote = self.create(original_input=original_input, search_params=search_params)
        quote.create_options()
        return quote
