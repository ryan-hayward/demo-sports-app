from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
from .models import Game
import pandas as pd
import numpy as np
import json

def index(request):
    return HttpResponse("Hello, World. Doing linear regression here.")

@api_view(['GET'])
# this API should be called with the structure 
def linear_regression(request):
    df = pd.DataFrame(list(Game.objects.all().values()))
    # get x and y var names
    x_var = request.GET.get('x_var')
    y_var = request.GET.get('y_var')
    # get series values from the dataframe
    x_series = df[x_var].values
    y_series = df[y_var].values
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
        'td_array': td_array
    })