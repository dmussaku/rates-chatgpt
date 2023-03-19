from datetime import date, timedelta
from decimal import Decimal
from random import randint

import factory
import factory.fuzzy
from faker import Faker

from . import models

fake = Faker()


class MainRateFactory(factory.django.DjangoModelFactory):
    carrier_id = factory.fuzzy.FuzzyChoice(models.CarrierIds)
    container_type = factory.fuzzy.FuzzyChoice(models.ContainerTypes)
    valid_from = factory.fuzzy.FuzzyDate(start_date=date(date.today().year, 1, 1))
    valid_until = factory.LazyAttribute(lambda o: o.valid_from + timedelta(weeks=4))
    pol = factory.SubFactory("rates.factories.PortFactory")
    pod = factory.SubFactory("rates.factories.PortFactory")

    class Meta:
        model = models.MainRate

    @factory.lazy_attribute
    def price(self):
        price_range_on_container_type = {
            models.ContainerTypes.TWENTY_FOOTER: (800, 1000),
            models.ContainerTypes.FOURTY_FOOTER: (1000, 1200),
            models.ContainerTypes.FOURTY_FOOTER_HC: (1200, 1500),
        }
        return Decimal(randint(*price_range_on_container_type[self.container_type]))


# create a factory for Surcharge model
class SurchargeFactory(factory.django.DjangoModelFactory):
    carrier_id = factory.fuzzy.FuzzyChoice(models.CarrierIds)
    valid_from = factory.fuzzy.FuzzyDate(start_date=date(date.today().year, 1, 1))
    valid_until = factory.LazyAttribute(lambda o: o.valid_from + timedelta(weeks=4))

    class Meta:
        model = models.Surcharge

    @factory.lazy_attribute
    def price(self):
        return Decimal(randint(100, 200))


# create a factory for Port model
class PortFactory(factory.django.DjangoModelFactory):
    country_code = factory.Sequence(lambda n: fake.country_code())
    code = factory.Sequence(lambda n: fake.country_code() + str(randint(100, 999)))
    name = factory.Sequence(lambda n: fake.city())

    class Meta:
        model = models.Port
