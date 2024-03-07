from django.urls import path
from . import views

urlpatterns = [
    # /analyzer/
    path("", views.index, name="index"),
    # /analyzer/timeframe
    path("linreg/", views.linear_regression, name="lin_reg")
]