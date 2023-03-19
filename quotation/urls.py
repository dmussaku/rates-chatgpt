# expose QuoteView in quotation app urls.py

# app/quotation/urls.py

from django.urls import path

from quotation.views import QuoteView


app_name = "quotation"
urlpatterns = [
    path("<str:quote_id>/", QuoteView.as_view(), name="quote"),
]
