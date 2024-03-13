from django.shortcuts import render
from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpResponse, JsonResponse
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
from .models import Game
import pandas as pd
import numpy as np

VALID_MODELS = ['Coach', 'Player', 'Game'] #@TODO add all valid models as they come in

def index(request):
    return HttpResponse("Hello, World. Doing linear regression here.")

@api_view(['GET'])
# this API should be called with the structure 
def linear_regression(request):
    # return error code if either expected param is absent
    if(request.GET.get('x_var') is None or request.GET.get('y_var') is None):
       return Response("Please ensure you have selected a dependent and independent variable.", status=400)

    df = pd.DataFrame(list(Game.objects.all().values()))
    # get x and y var names (hard code in defaults for testing purposes)
    x_var = request.GET.get('x_var') or 'home_pass_att'
    y_var = request.GET.get('y_var') or 'home_pass_yds'
    # get series values from the dataframe
    x_series = df[x_var].values
    y_series = df[y_var].values
    print(x_series.max(), y_series.max())
    # create 2d array to return to client
    td_array = np.column_stack((np.array(x_series), np.array(y_series)))
    # prepare model
    x = x_series.reshape(-1, 1)
    y = y_series.reshape(-1, 1)
    model = LinearRegression()
    model.fit(x,y)
    r2_score = model.score(x,y)

    return Response({
        'r2': r2_score, 
        'td_array': td_array,
        'x_max': x_series.max(),
        'y_max': y_series.max(),
        'x_var': x_var,
        'y_var': y_var
    })

@api_view(['GET'])
# standard search
# @TODO instead of hard-coding Game, make method model agnostic as get_filters is
def standard_search(request):
    tgt_model = request.GET.get('search_type')
    # mark invalid request if target model is specified incorrectly
    if tgt_model not in VALID_MODELS:
        return Response('Invalid search type.', status=400)

    # get a 2d array of all parameters besides the first (target model)
    param_list = []
    for k,v in request.GET.items():
        param_list.append([k, v])
    # ignore param specifying target model
    param_list = param_list[1:]
    # get target data given target model
    tgt_data = Game.objects.all()
    for param in param_list:
        filter = param[0]
        tgt_data = tgt_data.filter(**{filter: param[1]})
    # format data for return
    data = list(tgt_data.values())
    return JsonResponse(data, safe=False)


@api_view(['GET'])
# get eligible filters for a given model
# @TODO split model string to name conversion into a helper method that can be leveraged repeatedly
def get_filters(request):
    # try to get the model based on the string passed from client
    search_type = request.GET.get('search_type')
    # find the target model
    models = apps.get_models()
    tgt_model = None
    for model in models:
        if model.__name__ == search_type:
            tgt_model = model
            continue
    if tgt_model == None:
        return JsonResponse("Invalid model name. Select from dropdown.", safe=False)
    else:
        # get potential attrs to filter by from the model
        attr_list = [a.name for a in tgt_model._meta.get_fields()]
        return JsonResponse(attr_list, safe=False)