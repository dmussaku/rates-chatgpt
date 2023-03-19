# generate unit tests for the managers of the quotation app

# app/quotation/tests/test_managers.py
from django.test import TestCase
from quotation.factories import QuoteFactory, QuoteOptionFactory, QuoteLineItemFactory
from quotation.models import Quote, QuoteOption, QuoteLineItem


class QuoteManagerTestCase(TestCase):
    def setUp(self):
        self.quote = QuoteFactory()
        self.quote_option = QuoteOptionFactory(quote=self.quote)
        self.quote_line_item = QuoteLineItemFactory(quote_option=self.quote_option)

    def test_quote_manager(self):
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(Quote.objects.first(), self.quote)

    def test_quote_option_manager(self):
        self.assertEqual(QuoteOption.objects.count(), 1)
        self.assertEqual(QuoteOption.objects.first(), self.quote_option)

    def test_quote_line_item_manager(self):
        self.assertEqual(QuoteLineItem.objects.count(), 1)
        self.assertEqual(QuoteLineItem.objects.first(), self.quote_line_item)
