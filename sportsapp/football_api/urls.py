from django.urls import path
from . import views

# @TODO change "analyzer" to include api, since that is what it is
urlpatterns = [
    # /analyzer/
    path("", views.index, name="index"),
    # /analyzer/linreg
    path("linreg/", views.linear_regression, name="lin_reg"),
    # /analyzer/standard_search
    path("standard_search/", views.standard_search, name="std_search"),
    # /analyzer/get_filters
    path("get_filters/", views.get_filters, name="get_filters"),
    # /football-api/get_search_types
    path("get_search_types/", views.get_search_types, name='get_search_types')
]