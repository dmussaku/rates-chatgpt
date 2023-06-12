from django.test import TestCase


# generate me a test case for the rate model
class RateTestCase(TestCase):
    def setUp(self):
        Rate.objects.create(
            user_id=1,
            movie_id=1,
            rate=5
        )

    def test_rate(self):
        rate = Rate.objects.get(user_id=1)
        self.assertEqual(rate.rate, 5)