# -*- coding: utf-8 -*-
from mapclient.core import GEEApi
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_POST
def api(request):
    post = json.loads(request.body).get
    get = request.GET.get
    action = get('action', '')

    if action:
        public_methods = [
        'get-forest-extent-map', 'get-landcover', 'get-nightlight',
        'get-building-map', 'calMapArea', 'get-graph-data', 'get-val-map',
        'get-prop-map','get-graph-pie-data','get-nightlight-series', 'get-download-url'
        ]

        if action in public_methods:
            shape = post('shape', '')
            geom = post('polygon_id', '')
            area_path = post('areaSelectFrom', '')
            area_name = post('areaName', '')
            polygon_id=post('polygon_id', '')
            area_type=post('area_type', '')
            area_id=post('area_id', '')
            refLow=post('refLow', '')
            refHigh= post('refHigh', '')
            studyLow= post('studyLow', '')
            studyHigh=post('studyHigh', '')
            start_year = post('startYear', '')
            end_year = post('endYear', '')
            year = post('year', '')
            type = post('type', '')
            tree_canopy_definition = post('treeCanopyDefinition', 10) # in percentage
            tree_height_definition = post('treeHeightDefinition', 5) # in meters
            get_image = post('get_image', False)
            download  = post('download', '')
            data = post('data', '')
            feat = post('feat', '')
            lon = post('lon', '')
            lat = post('lat', '')

            core = GEEApi(area_path, area_name, geom, area_type, area_id)

            if action == 'get-forest-extent-map':
                data = core.get_mapid(type, start_year, end_year, tree_canopy_definition, tree_height_definition, area_type, area_id)
            elif action == 'get-landcover':
                data = core.getLandcoverArea(start_year, end_year, area_type, area_id)
            elif action == 'get-building-map':
                data = core.getOthersMap(area_type, area_id)
            elif action == 'calMapArea':
                data = core.getDataMap(start_year, end_year, area_type, area_id, data)
            elif action == 'get-graph-data':
                data = core.getGraphData(start_year, end_year, area_type, area_id, data)
            elif action == 'get-val-map':
                data = core.valnerabilityMap(feat, area_type, area_id)
            elif action == 'get-download-url':
                data = core.download_valnerabilityMap(type)
            elif action == 'get-graph-pie-data':
                data = core.getGraphPieData(area_type, area_id)
            elif action == 'get-prop-map':
                data = core.probabilityMaps()
            elif action =='get-nightlight':
                data = core.getNightLightWorldPopMap(start_year, end_year, area_type, area_id)
            elif action =='get-nightlight-series':
                data = core.getNightTimeSeriesVal(area_type, lon, lat)


            return JsonResponse(data, safe=False)
