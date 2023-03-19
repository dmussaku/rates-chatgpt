from functools import cached_property
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from quotation.managers import QuoteManager


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    search_params = models.JSONField(null=True, blank=True)

    objects = QuoteManager()


class QuoteOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="options")

    @property
    def total(self):
        return sum([item.total for item in self.line_items.all()])


class QuoteLineItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote_option = models.ForeignKey(
        QuoteOption, on_delete=models.CASCADE, related_name="line_items"
    )
    quantity = models.PositiveIntegerField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    @property
    def total(self):
        return self.quantity * self.content_object.price
