from django.shortcuts import render
from django.http import HttpResponse


import requests
import json
import datapackage
import pandas as pd
import plotly.express as px


# Create your views here.

def index(request):
    Token = 'PAGJgQkDGDdBFjRdEIvpKjailkQoXPLw'
    response = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GSOY&datatypeid=TAVG&startdate=2011-01-01&enddate=2020-01-01&stationid=GHCND:ASN00001020', headers = {'token': Token})
    data = json.loads(response.text)
    fig = px.line(data['results'], x='date', y='value', title='Average Temperature Annually')
    graph = fig.to_html(full_html = False, default_height = 500, default_width = 700)
    context = {'graph' : graph}
    return render(request, 'warm/index.html', context)

def ice(request):
    data_url = 'https://melted-polar-ice-cap.p.rapidapi.com/api/arctic-api'
    headers = {
        'x-rapidapi-host': "melted-polar-ice-cap.p.rapidapi.com",
        'x-rapidapi-key': "f7d52c6cdamshc15cf382f64212bp10ff26jsnd845601c0a02"
    }
    response = requests.request("GET", data_url, headers=headers)
    data = json.loads(response.text)
    fig = px.line(data['result'], x='year', y='extent', title = 'Annual Ice Extent')
    graph = fig.to_html(full_html = False, default_height = 500, default_width = 700)
    context = {'graph' : graph}
    return render(request, 'warm/ice.html', context)

def carbon(request):
    data_url = 'https://datahub.io/core/co2-ppm/datapackage.json'
    package = datapackage.Package(data_url)
    resources = package.resources
    data = pd.read_csv(resources[18].descriptor['path'])
    fig = px.line(data, x='Year', y='Mean', title='Carbon Emissions in PPM')
    graph = fig.to_html(full_html=False, default_height=500, default_width = 700)
    context = {'graph': graph}
    return render(request, 'warm/carbon.html', context)

def ocean(request):
    r = open('warm/ocean.json').read()
    data = json.loads(r)
    temparray = data['results']['bindings']
    dataarray = []
    for object in temparray:
        dataarray.append({'time': object['time']['value'], 'ph' : object['phcalc_insitu']['value']})
    fig = px.line(dataarray, x='time', y='ph', title = 'Ocean Acidification')
    graph = fig.to_html(full_html = False, default_height = 500, default_width = 700)
    context = {'graph': graph}
    return render(request, 'warm/ocean.html', context)