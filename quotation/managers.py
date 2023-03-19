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
        search_params: Dict,
        pol: Dict,
        pod: Dict,
        containers: List[Dict],  # [{"type": "20gp", "amount": 2, "goods": "apples"}]
        is_dangerous: bool,
        is_hazardous: bool,
        is_customs_needed: bool,
    ):
        quote = self.create(search_params=search_params)
        pols = Port.objects.filter_by_params(**pol)[:5]
        pods = Port.objects.filter_by_params(**pod)[:5]
        container_info = {obj["type"]: obj["amount"] for obj in containers}

        main_rates = MainRate.objects.filter(
            pol__in=pols, pod__in=pods, container_type__in=container_info.keys()
        )
        for main_rate in main_rates:
            quote_option = quote.options.create()
            quote_option.line_items.create(
                content_object=main_rate,
                quantity=container_info[main_rate.container_type],
            )
            if is_dangerous:
                surcharge = Surcharge.objects.get(
                    carrier_id=main_rate.carrier_id,
                    surcharge_type=SurchargeTypes.DANGEROUS_GOODS,
                )
                quote_option.line_items.create(
                    content_object=surcharge,
                    quantity=container_info[main_rate.container_type],
                )

            if is_customs_needed:
                surcharge = Surcharge.objects.get(
                    carrier_id=main_rate.carrier_id,
                    surcharge_type=SurchargeTypes.CUSTOMS_FEE,
                )
                quote_option.line_items.create(
                    content_object=surcharge,
                    quantity=container_info[main_rate.container_type],
                )
        return quote
