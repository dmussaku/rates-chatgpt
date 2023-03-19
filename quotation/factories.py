import factory
import factory.fuzzy

from django.contrib.contenttypes.models import ContentType
from quotation.models import Quote, QuoteOption, QuoteLineItem


class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quote


class QuoteOptionFactory(factory.django.DjangoModelFactory):
    quote = factory.SubFactory(QuoteFactory)

    class Meta:
        model = QuoteOption


class QuoteLineItemAbstractFactory(factory.django.DjangoModelFactory):
    quote_option = factory.SubFactory(QuoteOptionFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 100)

    object_id = factory.SelfAttribute("content_object.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )

    class Meta:
        exclude = ["content_object"]
        abstract = True


class QuoteMainRateLineItemFactory(QuoteLineItemAbstractFactory):
    content_object = factory.SubFactory("rates.factories.MainRateFactory")

    class Meta:
        model = QuoteLineItem


class QuoteSurchargeLineItemFactory(QuoteLineItemAbstractFactory):
    content_object = factory.SubFactory("rates.factories.SurchargeFactory")

    class Meta:
        model = QuoteLineItem
