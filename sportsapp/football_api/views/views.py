from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from sklearn.linear_model import LinearRegression
from ..models import Game
from ..serializers import GameSerializer, CoachSerializer, PlayerSerializer
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
def standard_search(request):
    search_type = request.GET.get('search_type')
    # find the target model
    tgt_model = get_model(search_type)
    # return error response if no model can be found
    if tgt_model == None:
        return Response(status=404)
    # get a 2d array of all parameters besides the first (target model)
    param_list = []
    for k,v in request.GET.items():
        param_list.append([k, v])
    # ignore param specifying target model
    param_list = param_list[1:]
    # get target data given target model
    tgt_data = tgt_model.objects.all()
    for param in param_list:
        filter = param[0]
        tgt_data = tgt_data.filter(**{filter: param[1]})
    # format data for return
    serializer = serialize_data(tgt_model, tgt_data)
    return Response(serializer.data)


@api_view(['GET'])
# get eligible filters for a given model
def get_filters(request):
    # try to get the model based on the string passed from client
    search_type = request.GET.get('search_type')
    # find the target model
    tgt_model = get_model(search_type)
    # return error response if no model can be found
    if tgt_model == None:
        return Response(status=404)
    else:
        # get potential attrs to filter by from the model
        attr_list = [a.name for a in tgt_model._meta.get_fields()]
        return JsonResponse(attr_list, safe=False)
    

@api_view(['GET'])
# get eligible models to search for
def get_search_types(request):
    # hard code for now
    # @TODO learn how to dynamically populate this list based on contents of the models
    return Response(VALID_MODELS)


# @TODO break off utils that the APIs use into a separate .py


# helper method to get target model based on string query param
def get_model(model_name: str):
    # initialize target model
    tgt_model = None
    models = apps.get_models()
    # loop through models until apprpriate model is found
    for model in models:
        if model.__name__ == model_name:
            tgt_model = model
            continue
    return tgt_model


# helper method to serialize data based on model specified in query params.
# takes Django Model and data as args and returns serialized data for response.
def serialize_data(model, data):
    # serialize data based on model
    if model.__name__ == 'Game':
        return GameSerializer(data, many=True)
    if model.__name__ == 'Coach':
        return CoachSerializer(data, many=True)
    if model.__name__ == 'PlayerBio':
        return PlayerSerializer(data, many=True)
    else:
        return None