from django.urls import path

from rates import views

urlpatterns = [
    path("", views.ChatView.as_view(), name="chat"),
]
