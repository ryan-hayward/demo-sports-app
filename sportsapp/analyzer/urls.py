from django.urls import path
from . import views

urlpatterns = [
    # /analyzer/
    path("", views.index, name="index"),
    # /analyzer/linreg
    path("linreg/", views.linear_regression, name="lin_reg"),
    # /analyzer/standard_search
    path("standard_search/", views.standard_search, name="std_search")
]