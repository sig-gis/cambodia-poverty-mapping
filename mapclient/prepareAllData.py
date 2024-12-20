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
import time

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

# BUILDING_FC = ee.FeatureCollection("projects/servir-mekong/buildings/cambodia")

SANITATION_IMG = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/AccesstoSanitation")

WATER_IMG  = ee.Image("projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Accesstocleanwater")

# VALNERABILITY_AMD3 = ee.FeatureCollection("projects/servir-mekong/undp/adm3_50v2/all_50")
# VALNERABILITY_AMD3 = ee.FeatureCollection("projects/servir-mekong/undp/website/adm3_50v2")
VALNERABILITY_AMD3 = ee.FeatureCollection("projects/servir-mekong/undp/website/basemap/adm3_19")
VALNERABILITY_AMD3_19 = ee.FeatureCollection("projects/servir-mekong/undp/website/basemap/adm3_19")
VALNERABILITY_AMD3_22 = ee.FeatureCollection("projects/servir-mekong/undp/website/basemap/adm3_22")
VALNERABILITY_AMD3_23 = ee.FeatureCollection("projects/servir-mekong/undp/website/basemap/adm3_23")


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
data_year = 0

# Perform a join to add DIST_NAME to VALNERABILITY_AMD3
def add_district_name(feature):
    # Get the DIS_CODE from the sub-district
    dis_code = feature.get('DIS_CODE')
    
    # Find the corresponding district feature
    district = ADM2.filter(ee.Filter.eq('DIS_CODE', dis_code)).first()
    
    # Get the DIST_NAME from the district
    dist_name = ee.String(district.get('DIS_NAME'))
    
    # Add DIST_NAME to the sub-district feature
    return feature.set('DIS_NAME', dist_name)

#--------------------------------------------------------------------------

def nightlight(series_start, series_end, _year):
    nightlight = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG").select("avg_rad")
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

def allArea(prov, data_year):
    # Ensure data_year is valid
    if data_year == 2019:
        provAll = VALNERABILITY_AMD3_19.filterBounds(prov.geometry())
    elif data_year == 2022:
        provAll = VALNERABILITY_AMD3_22.filterBounds(prov.geometry())
    elif data_year == 2023:
        provAll = VALNERABILITY_AMD3_23.filterBounds(prov.geometry())
    else:
        raise ValueError(f"Unsupported year: {data_year}. Please use 2019, 2022, or 2023.")

    # Perform aggregation
    total = provAll.aggregate_sum("Total")
    Education = provAll.aggregate_sum("Education0")
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

    return prov.set("Total", ee.Number(1).subtract(Education.divide(total)))\
               .set("Education0", ee.Number(1).subtract(Education.divide(total)))\
               .set("edu_attain0", ee.Number(1).subtract(edu_attain.divide(total)))\
               .set("edu_attend0", ee.Number(1).subtract(edu_attend.divide(total)))\
               .set("Health0", ee.Number(1).subtract(Health.divide(total)))\
               .set("health_access0", ee.Number(1).subtract(healt_access.divide(total)))\
               .set("health_food0", ee.Number(1).subtract(healt_food.divide(total)))\
               .set("health_handwash0", ee.Number(1).subtract(healt_handWash.divide(total)))\
               .set("health_sanit0", ee.Number(1).subtract(healt_sanit.divide(total)))\
               .set("health_water0", ee.Number(1).subtract(healt_water.divide(total)))\
               .set("LivingStandard0", ee.Number(1).subtract(LivingStandard.divide(total)))\
               .set("liv_asset0", ee.Number(1).subtract(liv_asset.divide(total)))\
               .set("liv_cooking0", ee.Number(1).subtract(liv_cooking.divide(total)))\
               .set("liv_coping0", ee.Number(1).subtract(liv_coping.divide(total)))\
               .set("liv_elect0", ee.Number(1).subtract(liv_elect.divide(total)))\
               .set("liv_hous0", ee.Number(1).subtract(liv_house.divide(total)))\
               .set("liv_overcr0", ee.Number(1).subtract(liv_overcrowd.divide(total)))\
               .set("Monetary0", ee.Number(1).subtract(monetary.divide(total)))\
               .set("overall0", ee.Number(1).subtract(overall.divide(total)))


def calfraction(self, feat):
    total = ee.Number(feat.get("Total")).float()
    sample = ee.Number(feat.get(self.feat_name)).float()
    return feat.set("Not Deprived",ee.Number(1).subtract(sample.divide(total))).set("Deprived",sample.divide(total))

def main(area_type, year):
    data_year = year
  
    feat_names = ['Education0', 'Health0', 'LivingStandard0', 'Monetary0', 'Total', 'Unemploy0', 'edu_attain0', 'edu_attend0', 'health_access0', 'health_food0', 'health_handwash0', 'health_sanit0', 'health_water0', 'liv_asset0', 'liv_cooking0', 'liv_coping0', 'liv_elect0', 'liv_hous0', 'liv_overcr0', 'overall0', 'underemployment0', 'unemploy0']
    res = {}
    adm_name = ''
    
    if (data_year == 2019):
        VALNERABILITY_AMD3 = VALNERABILITY_AMD3_19
    elif (data_year == 2022):
        VALNERABILITY_AMD3 = VALNERABILITY_AMD3_22
    elif (data_year == 2023):
        VALNERABILITY_AMD3 = VALNERABILITY_AMD3_23

    for feat_name in feat_names:
        _feat_name = feat_name

        _Deprived = []
        _Not_Deprived = []
        
        if area_type == "sub-district":
            val_map = VALNERABILITY_AMD3 #self.getFraction(VALNERABILITY_AMD3, feat_name)
            adm_name = 'COM_NAME'
            adm_id = 'COM_CODE'
            _json = 'VALNERABILITY_DATA_AMD3_'+year+'.json'
            obj = val_map.aggregate_array(feat_name).getInfo()
            total = val_map.aggregate_array("Total").getInfo()
            no_pop = POP_ADM3.aggregate_array("population").getInfo()
            no_buildings = POP_ADM3.aggregate_array("buildingCount").getInfo()
            for i in range(len(obj)):
                if total[i] != 0:
                    _Not_Deprived.append(1 - (obj[i] / total[i]))
                    _Deprived.append(obj[i] / total[i])
                else:
                    _Not_Deprived.append(1)
                    _Deprived.append(0) 

        elif area_type == "district":
            batch_size = 50
            ADM2_list = ADM2.toList(ADM2.size())  # Convert entire collection to a list
            results = []

            # Process features in batches
            for i in range(0, ADM2.size().getInfo(), batch_size):
                subset = ee.FeatureCollection(ADM2_list.slice(i, i + batch_size))
                subset_result = subset.map(lambda prov: allArea(prov, data_year))
                results.append(subset_result)

            # Combine results into one FeatureCollection
            val_map = ee.FeatureCollection(results).flatten()

            # Aggregate values
            adm_name = 'DIS_NAME'
            adm_id = 'DIS_CODE'
            _json = 'VALNERABILITY_DATA_AMD2_' + str(year) + '.json'

            # Check if feat_name exists
            obj = val_map.aggregate_array(feat_name).getInfo()

            no_pop = []
            no_buildings = []
            for val in obj:
                _Not_Deprived.append(val)
                _Deprived.append(1 - val)

        
        elif area_type == "province":
            val_map = ADM1.map(lambda prov: allArea(prov, data_year))
            adm_name = 'HRName'
            adm_id = 'PRO_CODE'
            _json = 'VALNERABILITY_DATA_AMD1_'+str(year)+'.json'
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
    

    res['name_area'] = list(val_map.aggregate_array(adm_name).getInfo())
    res['id_area'] = list(val_map.aggregate_array(adm_id).getInfo())
    res['population'] = list(no_pop)
    res['buildings'] = list(no_buildings)


    with open("../povertymappingapp/static/data/"+_json, 'w', encoding='utf8') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
        print(f"create a json file: {_json}")

if __name__ == "__main__":
    main("sub-district", 2019)
    main("sub-district", 2022)
    main("sub-district", 2023)
    
    main("province", 2019)
    main("province", 2022)
    main("province", 2023)

    main("district", 2019)
    main("district", 2022)
    main("district", 2023)