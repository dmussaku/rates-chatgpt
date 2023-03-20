import itertools
from functools import cached_property
from typing import List
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from rates.models import MainRate, Surcharge, Port, ContainerTypes, CarrierIds, SurchargeTypes
from quotation.managers import QuoteManager


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_input = models.TextField(null=True, blank=True)
    search_params = models.JSONField(null=True, blank=True)

    objects = QuoteManager()

    def recreate_options(self):
        self.delete_options()
        self.create_options()

    def delete_options(self):
        self.options.all().delete()

    def create_options(self):
        pol = self.search_params["pol"]
        pod = self.search_params["pod"]
        containers = self.search_params["containers"]


        pols = Port.objects.filter_by_params(**pol)[:3]
        pods = Port.objects.filter_by_params(**pod)[:3]
        container_info = {obj["type"]: obj["amount"] for obj in containers}
        pol_pod_carrier_ids = MainRate.objects.filter(
            pol__in=pols, pod__in=pods, container_type__in=container_info.keys()
        ).values_list('pol', 'pod', 'carrier_id').distinct()

        for pol, pod, carrier_id in pol_pod_carrier_ids.distinct():
            print (pol, pod, carrier_id)
            main_rates = MainRate.objects.filter(pol=pol, pod=pod, carrier_id=carrier_id, container_type__in=container_info.keys())
            quote_option = self.options.create()

            for container in containers:
                print(main_rates)
                main_rate = main_rates.get(container_type=container["type"])
                quote_option.line_items.create(
                    content_object=main_rate,
                    quantity=container['amount'],
                    goods=','.join(container['goods_names']),
                )
                if container.get("is_dangerous", False):
                    surcharge = Surcharge.objects.get(
                        carrier_id=main_rate.carrier_id,
                        surcharge_type=SurchargeTypes.DANGEROUS_GOODS,
                    )
                    quote_option.line_items.create(
                        content_object=surcharge,
                        quantity=container['amount'],
                        goods=','.join(container['goods_names']),
                    )

                if container.get("is_customs_needed", False):
                    surcharge = Surcharge.objects.get(
                        carrier_id=main_rate.carrier_id,
                        surcharge_type=SurchargeTypes.CUSTOMS_FEE,  
                    )
                    quote_option.line_items.create(
                        content_object=surcharge,
                        quantity=container['amount'],
                        goods=','.join(container['goods_names']),
                    )
                if container.get("is_fragile", False):
                    surcharge = Surcharge.objects.get(
                        carrier_id=main_rate.carrier_id,
                        surcharge_type=SurchargeTypes.FRAGILE_FEE,
                    )
                    quote_option.line_items.create(
                        content_object=surcharge,
                        quantity=container['amount'],
                        goods=','.join(container['goods_names']),
                    )
                

class QuoteOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="options")

    @property
    def total(self):
        return sum([item.total for item in self.line_items.all()])

    @property
    def main_rates_line_items(self):
        return self.line_items.filter(content_type=ContentType.objects.get_for_model(MainRate))

    @property
    def surcharges_line_items(self):
        return self.line_items.filter(content_type=ContentType.objects.get_for_model(Surcharge))


class QuoteLineItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote_option = models.ForeignKey(
        QuoteOption, on_delete=models.CASCADE, related_name="line_items"
    )
    quantity = models.PositiveIntegerField()
    goods = models.TextField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    @property
    def total(self):
        return self.quantity * self.content_object.price
