from django.urls import path
from . import views

urlpatterns = [
    path("pay/<slug:slug>/", views.create_payment, name="create_payment"),
    path("execute/<slug:slug>/", views.execute_payment, name="payment_execute"),
    path("cancel/<slug:slug>/", views.payment_cancel, name="payment_cancel"),
    path("success/<slug:slug>/", views.payment_success, name="payment_success"),
]
