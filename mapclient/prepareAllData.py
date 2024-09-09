# -*- coding: utf-8 -*-
from django.core import serializers
from django.http import HttpResponse
import datetime
import numpy as np
import base64
from django.conf import settings
import ee, json, os, time
from django.http import JsonResponse
from django.http import HttpResponse
from ee.ee_exception import EEException
import requests
import json
from google.oauth2 import service_account

# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# EE_ACCOUNT = 'me-cambodia-dashboard@me-cambodia-dashboard.iam.gserviceaccount.com'
EE_ACCOUNT = 'khpovertymapping@servir-ee.iam.gserviceaccount.com'
# The private key associated with your service account in Privacy Enhanced
# Email format (deprecated version .pem suffix, new version .json suffix).
EE_PRIVATE_KEY_FILE = os.path.join(BASE_DIR, 'credentials/privatekey.json')
# Service account scope for GEE

GOOGLE_EARTH_SCOPES = ('https://www.googleapis.com/auth/earthengine',)

GOOGLE_OAUTH2_SCOPES = ('https://www.googleapis.com/auth/drive',
                        'profile',
                        'email',
                        )
EE_CREDENTIALS = ee.ServiceAccountCredentials(EE_ACCOUNT, EE_PRIVATE_KEY_FILE)

# ee.Initialize(settings.EE_CREDENTIALS)
ee.Initialize(EE_CREDENTIALS)
# image collection

scale = 100
HEALTH_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Accesstohealthcare")
# Map.addLayer(health,{min:20,max:80,palette:"darkgreen,green,yellow,orange,red,darkred"},"health",false);
#public service
ASSETS_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Assets")
#public service
FUEL_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Cookingfuel")
#education
EDUCATION_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/EducationalAttainment")
#public service
FOOD_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/FoodConsumptionScore")
#housing
HOUSING_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Housingmaterials")
#education
SCHOOL_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/SchoolAttendance")
#public service
ELECTRICITY_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/accesstoelectricity")
#income
CONSUMPTION_IMG = ee.Image("projects/servir-mekong/undp/indicators/ConsumptionandExpenditure")

BUILDING_FC = ee.FeatureCollection("projects/servir-mekong/buildings/cambodia")

SANITATION_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/AccesstoSanitation")

WATER_IMG  = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Accesstocleanwater")

# VALNERABILITY_AMD3 = ee.FeatureCollection("projects/servir-mekong/undp/adm3_50v2/all_50")
VALNERABILITY_AMD3 = ee.FeatureCollection("projects/servir-mekong/undp/website/adm3_50v2")

# ADM3 = ee.FeatureCollection("projects/earthengine-legacy/assets/projects/servir-mekong/admin/KHM_adm3")
# ADM2 = ee.FeatureCollection("projects/earthengine-legacy/assets/projects/servir-mekong/admin/KHM_adm2")
# ADM1 = ee.FeatureCollection("projects/earthengine-legacy/assets/projects/servir-mekong/admin/KHM_adm1")
# ADM0 = ee.FeatureCollection("projects/earthengine-legacy/assets/projects/servir-mekong/admin/KHM_adm0")

ADM3 = ee.FeatureCollection("projects/earthengine-legacy/assets/projects/servir-mekong/undp/website/basemap/adm3")
ADM2 = ee.FeatureCollection("projects/earthengine-legacy/assets/projects/servir-mekong/undp/website/basemap/adm2")
ADM1 = ee.FeatureCollection("projects/earthengine-legacy/assets/projects/servir-mekong/undp/website/basemap/adm1")
ADM0 = ee.FeatureCollection("projects/earthengine-legacy/assets/projects/servir-mekong/admin/KHM_adm0")

POP_ADM1 = ee.FeatureCollection("projects/servir-mekong/undp/website/populationAdm1")
POP_ADM2 = ee.FeatureCollection("projects/servir-mekong/undp/website/populationAdm2")
POP_ADM3 = ee.FeatureCollection("projects/servir-mekong/undp/website/populationAdm3")
BUILDINGS_POP = ee.Image("projects/servir-mekong/undp/buildingsWithPeople/buildingsWithPeopleImg")


_feat_name = ""
#--------------------------------------------------------------------------

def nightlight(series_start, series_end, _year):
    nightlight = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG").select("avg_rad");
    nightlightImg = nightlight.select("avg_rad").filterDate(series_start, series_end).mean().select("avg_rad").clip(ADM0.geometry());
    map_id = nightlightImg.getMapId({
        'min': '0',
        'max': '10',
        'palette': '000000,700000,808080,FFFF00,ffffff,ffffff,ffffff'
    })
    obj = {
        'eeMapId': str(map_id['mapid']),
        'eeMapURL': str(map_id['tile_fetcher'].url_format),
    }
    return obj


# -------------------------------------------------------------------------
def getNightLightMap(start_year, end_year, area_type, area_id):
    res = {}
    for _year in range(start_year, end_year+1):
        series_start = str(_year) + '-01-01'
        series_end = str(_year) + '-12-31'
        res[str(_year)] = nightlight(series_start, series_end, _year, area_type, area_id)
    return res
#--------------------------------------------------------------------------

def allArea(prov):
    provAll = VALNERABILITY_AMD3.filterBounds(prov.geometry())

    total = provAll.aggregate_sum("Total")
    Education =   provAll.aggregate_sum("Education0")
    edu_attain = provAll.aggregate_sum("edu_attain0")
    edu_attend = provAll.aggregate_sum("edu_attend0")
    Health = provAll.aggregate_sum("Health0")
    healt_access = provAll.aggregate_sum("health_access0")
    healt_food = provAll.aggregate_sum("health_food0")
    healt_handWash = provAll.aggregate_sum("health_handwash0")
    healt_sanit = provAll.aggregate_sum("health_sanit0")
    healt_water = provAll.aggregate_sum("health_water0")
    LivingStandard = provAll.aggregate_sum("LivingStandard0")
    liv_asset = provAll.aggregate_sum("liv_asset0")
    liv_cooking = provAll.aggregate_sum("liv_cooking0")
    liv_coping = provAll.aggregate_sum("liv_coping0")
    liv_elect = provAll.aggregate_sum("liv_elect0")
    liv_house = provAll.aggregate_sum("liv_hous0")
    liv_overcrowd = provAll.aggregate_sum("liv_overcr0")
    monetary = provAll.aggregate_sum("Monetary0")
    overall = provAll.aggregate_sum("overall0")


    return prov.set("Total",ee.Number(1).subtract(Education.divide(total)))\
    .set("Education0",ee.Number(1).subtract(Education.divide(total)))\
    .set("edu_attain0",ee.Number(1).subtract(edu_attain.divide(total)))\
    .set("edu_attend0",ee.Number(1).subtract(edu_attend.divide(total)))\
    .set("Health0",ee.Number(1).subtract(Health.divide(total)))\
    .set("health_access0",ee.Number(1).subtract(healt_access.divide(total)))\
    .set("health_food0",ee.Number(1).subtract(healt_food.divide(total)))\
    .set("health_handwash0",ee.Number(1).subtract(healt_handWash.divide(total)))\
    .set("health_sanit0",ee.Number(1).subtract(healt_sanit.divide(total)))\
    .set("health_water0",ee.Number(1).subtract(healt_water.divide(total)))\
    .set("LivingStandard0",ee.Number(1).subtract(LivingStandard.divide(total)))\
    .set("liv_asset0",ee.Number(1).subtract(liv_asset.divide(total)))\
    .set("liv_cooking0",ee.Number(1).subtract(liv_cooking.divide(total)))\
    .set("liv_coping0",ee.Number(1).subtract(liv_coping.divide(total)))\
    .set("liv_elect0",ee.Number(1).subtract(liv_elect.divide(total)))\
    .set("liv_hous0",ee.Number(1).subtract(liv_house.divide(total)))\
    .set("liv_overcr0",ee.Number(1).subtract(liv_overcrowd.divide(total)))\
    .set("Monetary0",ee.Number(1).subtract(monetary.divide(total)))\
    .set("overall0",ee.Number(1).subtract(overall.divide(total)))

def calfraction(self, feat):
    total = ee.Number(feat.get("Total")).float()
    sample = ee.Number(feat.get(self.feat_name)).float()
    return feat.set("Not Deprived",ee.Number(1).subtract(sample.divide(total))).set("Deprived",sample.divide(total))

area_type = "province"

def main(area_type):
    feat_names = ['Education0', 'Health0', 'LivingStandard0', 'Monetary0', 'Total', 'Unemploy0', 'edu_attain0', 'edu_attend0', 'health_access0', 'health_food0', 'health_handwash0', 'health_sanit0', 'health_water0', 'liv_asset0', 'liv_cooking0', 'liv_coping0', 'liv_elect0', 'liv_hous0', 'liv_overcr0', 'overall0', 'underemployment0', 'unemploy0']

    res = {}
    adm_name = ''
    for feat_name in feat_names:
        _feat_name = feat_name
        print(feat_name)
        _Deprived = []
        _Not_Deprived = []
        
        if area_type == "sub-district":
            val_map = VALNERABILITY_AMD3 #self.getFraction(VALNERABILITY_AMD3, feat_name)
            adm_name = 'COM_NAME'
            adm_id = 'COM_CODE'
            _json = 'VALNERABILITY_DATA_AMD3_v2.json'
            obj = val_map.aggregate_array(feat_name).getInfo()
            total = val_map.aggregate_array("Total").getInfo()
            no_pop = POP_ADM3.aggregate_array("population").getInfo()
            no_buildings = POP_ADM3.aggregate_array("buildingCount").getInfo()

            for i in range(len(obj)):
                if total[i] != 0:
                    _Not_Deprived.append(1 - (obj[i] / total[i]))
                    _Deprived.append(obj[i] / total[i])
                else:
                    # Handle the zero division case appropriately
                    _Not_Deprived.append(1)  # Assuming a default value
                    _Deprived.append(0)      # Assuming a default value
            # _arr.append(dict)

        elif area_type == "district":
            val_map = ADM2.map(allArea)
            adm_name = 'HRName'
            adm_id = 'DIS_CODE'
            _json = 'VALNERABILITY_DATA_AMD2_v2.json'
            obj = val_map.aggregate_array(feat_name).getInfo()
            # no_pop = POP_DM2.aggregate_array("population").getInfo()
            # no_buildings = POP_ADM2.aggregate_array("buildingCount").getInfo()
            no_pop = []
            no_buildings = []
            for val in obj:
                _Not_Deprived.append(val)
                _Deprived.append(1-val)
        
        elif area_type == "province":
            val_map = ADM1.map(allArea)
            adm_name = 'HRName'
            adm_id = 'HRPCode'
            _json = 'VALNERABILITY_DATA_AMD1_v2.json'
            obj = val_map.aggregate_array(feat_name).getInfo()
            no_pop = POP_ADM1.aggregate_array("population").getInfo()
            no_buildings = POP_ADM1.aggregate_array("buildingCount").getInfo()
            for val in obj:
                _Not_Deprived.append(val)
                _Deprived.append(1-val)
        dict = {
            "Not Deprived": _Not_Deprived,
            "Deprived": _Deprived
        }
        
        res[feat_name] = dict
    
    res['name_area'] = val_map.aggregate_array(adm_name).getInfo()
    res['id_area'] = val_map.aggregate_array(adm_id).getInfo()
    res['population'] = no_pop
    res['buildings'] = no_buildings


    with open("../povertymappingapp/static/data/"+_json, 'w', encoding='utf8') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
        print(f"create a json file: {_json}")

if __name__ == "__main__":
    # main("sub-district")
    main("district")
    # main("province")
