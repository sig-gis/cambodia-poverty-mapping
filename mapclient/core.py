# -*- coding: utf-8 -*-
from django.conf import settings
import ee

# -----------------------------------------------------------------------------
class GEEApi():
    """ Google Earth Engine API """
    # ee.Initialize(settings.EE_CREDENTIALS)
    ee.Initialize(settings.EE_CREDENTIALS)
    COLOR = ['A8D9C6','B0DAB2','BFE1C9','AAD7A0','C3DE98','D5E59E','93D2BF','95CF9C','A4D7B8','9BD291','B1D78A','C9E08E','5CC199','77C78C','37B54A','126039','146232','0F8040','279445','449644','59A044','0E361E','236832','335024', '36461F']
    COLORFORESTALERT = ['943126', 'B03A2E', 'CB4335', 'E74C3C', 'F1948A', 'F5B7B1','943126', 'B03A2E', 'CB4335', 'E74C3C', 'F1948A', 'F5B7B1']
    COLORSARALERT = ['fba004', 'f9bc16', 'ac9d0a', 'fba004', 'f9bc16', 'ac9d0a','fba004', 'f9bc16', 'ac9d0a','fba004', 'f9bc16', 'ac9d0a']

    def __init__(self, area_path, area_name, geom, area_type, area_id):
        self.scale = 100
        self.VAL_YEAR = 2023

        # image collection
        self.LANDCOVER = ee.ImageCollection(settings.LANDCOVER)
        self.VALNERABILITY_AMD3_19 = ee.FeatureCollection(settings.VALNERABILITY_AMD3_19)
        self.VALNERABILITY_AMD3_22 = ee.FeatureCollection(settings.VALNERABILITY_AMD3_22)
        self.VALNERABILITY_AMD3_23 = ee.FeatureCollection(settings.VALNERABILITY_AMD3_23)
        self.ADM3 = ee.FeatureCollection(settings.ADM3)
        self.ADM2 = ee.FeatureCollection(settings.ADM2)
        self.ADM1 = ee.FeatureCollection(settings.ADM1)
        self.ADM0 = ee.FeatureCollection(settings.ADM0)
        self.geometry = self.ADM0.geometry()

        self.POP_ADM1 = ee.FeatureCollection(settings.POP_ADM1)
        self.POP_ADM2 = ee.FeatureCollection(settings.POP_ADM2)
        self.POP_ADM3 = ee.FeatureCollection(settings.POP_ADM3)
        self.BUILDINGS_POP = ee.Image(settings.BUILDINGS_POP)
        self.DEPRIVATIONIMG = ee.Image(settings.DEPRIVATIONIMG)
        self.NIGHTLIGHT = ee.ImageCollection(settings.NIGHTLIGHT).select("avg_rad")
        self.WORLDPOP = ee.ImageCollection(settings.WORLDPOP)

        #indicators 2019
        self.buildings = ee.FeatureCollection(settings.BUILDINGS)
        self.Education19 = ee.Image(settings.IMG_EDUCATION19)
        self.food19 = ee.Image(settings.IMG_FOOD19)
        self.Health19 = ee.Image(settings.IMG_HEALTH19)
        self.water19 = ee.Image(settings.IMG_WATER19)
        self.sanitation19 = ee.Image(settings.IMG_SANITATION19)
        self.handWashing19 = ee.Image(settings.IMG_HANDWASHING19)
        # self.Health19 = ee.Image(self.food.add(self.health).add(self.water).add(self.sanitation).add(self.handWashing)).divide(5)
        self.overcrowding19 = ee.Image(settings.IMG_OVERCROWDING19)
        self.housing19 = ee.Image(settings.IMG_HOUSING19)
        self.fuel19 = ee.Image(settings.IMG_FUEL19)
        self.electricity19 = ee.Image(settings.IMG_ELECTRICITY19)
        self.assets19 = ee.Image(settings.IMG_ASSETS19)
        self.livelihoodBasedCopingStrategies19 = ee.Image(settings.IMG_LIVELIHOODBASEDCOPINGSTRATEGIES19)
        self.LivingStandard19 = ee.Image(self.overcrowding19.add(self.housing19).add(self.fuel19).add(self.electricity19).add(self.assets19).add(self.livelihoodBasedCopingStrategies19)).divide(6)
        self.consumption19 = ee.Image(settings.IMG_CONSUMPTION19)
        self.totalV219 = ee.Image(settings.IMG_TOTALV219)

        #indicators 2022
        self.Education22 = ee.Image(settings.IMG_EDUCATION22)
        self.food22 = ee.Image(settings.IMG_FOOD22)
        self.Health22 = ee.Image(settings.IMG_HEALTH22)
        self.water22 = ee.Image(settings.IMG_WATER22)
        self.sanitation22 = ee.Image(settings.IMG_SANITATION22)
        self.handWashing22 = ee.Image(settings.IMG_HANDWASHING22)
        # self.Health22 = ee.Image(self.food.add(self.health).add(self.water).add(self.sanitation).add(self.handWashing)).divide(5)
        self.overcrowding22 = ee.Image(settings.IMG_OVERCROWDING22)
        self.housing22 = ee.Image(settings.IMG_HOUSING22)
        self.fuel22 = ee.Image(settings.IMG_FUEL22)
        self.electricity22 = ee.Image(settings.IMG_ELECTRICITY22)
        self.assets22 = ee.Image(settings.IMG_ASSETS22)
        self.livelihoodBasedCopingStrategies22 = ee.Image(settings.IMG_LIVELIHOODBASEDCOPINGSTRATEGIES22)
        self.LivingStandard22 = ee.Image(self.overcrowding22.add(self.housing22).add(self.fuel22).add(self.electricity22).add(self.assets22).add(self.livelihoodBasedCopingStrategies22)).divide(6)
        self.consumption22 = ee.Image(settings.IMG_CONSUMPTION22)
        self.totalV222 = ee.Image(settings.IMG_TOTALV222)

        #indicators 2023
        self.Education23 = ee.Image(settings.IMG_EDUCATION23)
        self.food23 = ee.Image(settings.IMG_FOOD23)
        self.Health23 = ee.Image(settings.IMG_HEALTH23)
        self.water23 = ee.Image(settings.IMG_WATER23)
        self.sanitation23 = ee.Image(settings.IMG_SANITATION23)
        self.handWashing23 = ee.Image(settings.IMG_HANDWASHING23)
        # self.Health23 = ee.Image(self.food.add(self.health).add(self.water).add(self.sanitation).add(self.handWashing)).divide(5)
        self.overcrowding23 = ee.Image(settings.IMG_OVERCROWDING23)
        self.housing23 = ee.Image(settings.IMG_HOUSING23)
        self.fuel23 = ee.Image(settings.IMG_FUEL23)
        self.electricity23 = ee.Image(settings.IMG_ELECTRICITY23)
        self.assets23 = ee.Image(settings.IMG_ASSETS23)
        self.livelihoodBasedCopingStrategies23 = ee.Image(settings.IMG_LIVELIHOODBASEDCOPINGSTRATEGIES23)
        self.LivingStandard23 = ee.Image(self.overcrowding23.add(self.housing23).add(self.fuel23).add(self.electricity23).add(self.assets23).add(self.livelihoodBasedCopingStrategies23)).divide(6)
        self.consumption23 = ee.Image(settings.IMG_CONSUMPTION23)
        self.totalV223 = ee.Image(settings.IMG_TOTALV223)

    #--------------------------------------------------------------------------
    def get_NightlightWorldPop(self, series_start, series_end, _year, area_type, area_id):
        nightlight = self.NIGHTLIGHT.filterBounds(self.ADM0.geometry())
        worldpop = self.WORLDPOP.filterBounds(self.ADM0.geometry())

        nightlightImg = nightlight.select("avg_rad").filterDate(series_start, series_end).mean().select("avg_rad").clip(self.ADM0.geometry())
        worldpopImg = worldpop.filterDate(series_start, series_end).mean().clip(self.ADM0.geometry())

        map_id_nightlight = nightlightImg.getMapId({
            'min': '0',
            'max': '10',
            'palette': '000000,700000,808080,FFFF00,ffffff,ffffff,ffffff'
        })

        map_id_worldpop = worldpopImg.getMapId({
            'min': '0',
            'max': '50',
            'palette': '000000,700000,808080,FFFF00,ffffff,ffffff,ffffff'
        })

        obj = {
        "Nightlight":
            {
                'mapID': "nightlight",
                'eeMapId': str(map_id_nightlight['mapid']),
                'eeMapURL': str(map_id_nightlight['tile_fetcher'].url_format),
            },
        "WorldPop":
            {
                'mapID': "worldpop",
                'eeMapId': str(map_id_worldpop['mapid']),
                'eeMapURL': str(map_id_worldpop['tile_fetcher'].url_format),
            },
        }
        return obj


    # -------------------------------------------------------------------------
    def getNightLightWorldPopMap(self, start_year, end_year, area_type, area_id):
        res = {}
        for _year in range(start_year, end_year+1):
            series_start = str(_year) + '-01-01'
            series_end = str(_year) + '-12-31'
            res[str(_year)] = self.get_NightlightWorldPop(series_start, series_end, _year, area_type, area_id)
        return res
    #--------------------------------------------------------------------------

    def allArea(self, prov):
        if(self.VAL_YEAR == 2019):
            VAL_FEAT = self.VALNERABILITY_AMD3_19
        elif(self.VAL_YEAR == 2022):
            VAL_FEAT = self.VALNERABILITY_AMD3_22
        elif(self.VAL_YEAR == 2023):
            VAL_FEAT = self.VALNERABILITY_AMD3_23
  
        provAll = VAL_FEAT.filterBounds(prov.geometry())
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
    
    def allArea19(self, prov):
        provAll = self.VALNERABILITY_AMD3_19.filterBounds(prov.geometry())
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

    def allArea22(self, prov):
        provAll = self.VALNERABILITY_AMD3_22.filterBounds(prov.geometry())
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
    
    def allArea23(self, prov):
        provAll = self.VALNERABILITY_AMD3_23.filterBounds(prov.geometry())
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

    def calDeprived(self, feat):
        feat = feat.set("Not Deprived",ee.Number(feat.get(self.feat_name)))
        feat = feat.set("Deprived",ee.Number(1).subtract(ee.Number(feat.get(self.feat_name))))
        return feat

    def getFraction(self, ft, featureName):
        self.featureName= featureName
        ft = ft.map(self.calfraction)
        return ft
    
    def getValFeat(self, year):
        if(year == 2019):
            return self.VALNERABILITY_AMD3_19
        elif(year == 2022):
            return self.VALNERABILITY_AMD3_22
        elif(year == 2023):
            return self.VALNERABILITY_AMD3_23

    def valnerabilityMap(self, area_type, year):
        feat_names = ["Education0", "edu_attain0", "edu_attend0",
        "Health0", "health_food0", "health_access0", "health_water0","health_sanit0", "health_handwash0",
        "LivingStandard0", "liv_overcr0", "liv_hous0", "liv_cooking0", "liv_elect0", "liv_asset0", "liv_coping0",
        "Monetary0", "overall0"]
        res = {}
        adm_name = ''
        
        self.val_year = year

        VAL_FEAT = self.getValFeat(year)
        
        for feat_name in feat_names:
            self.feat_name = feat_name
            if area_type == "sub-district":
                val_map = self.getFraction(VAL_FEAT, self.feat_name)
                img = val_map.reduceToImage(
                    properties= ["Not Deprived"],
                    reducer= ee.Reducer.mean(),
                )
                adm_name = 'NAME_3'
            elif area_type == "country":
                if(year == 2019):
                    val_map = self.ADM0.map(self.allArea19)
                elif(year == 2022):
                    val_map = self.ADM0.map(self.allArea22)
                elif(year == 2023):
                    val_map = self.ADM0.map(self.allArea23)
    
                img = val_map.reduceToImage([self.feat_name],ee.Reducer.mean())
                adm_name = 'NAME_0'
            elif area_type == "province":
                if(year == 2019):
                    val_map = self.ADM1.map(self.allArea19)
                elif(year == 2022):
                    val_map = self.ADM1.map(self.allArea22)
                elif(year == 2023):
                    val_map = self.ADM1.map(self.allArea23)
                img = val_map.reduceToImage([self.feat_name],ee.Reducer.mean())
                adm_name = 'NAME_1'
            elif area_type == "district":
                if(year == 2019):
                    val_map = self.ADM2.map(self.allArea19)
                elif(year == 2022):
                    val_map = self.ADM2.map(self.allArea22)
                elif(year == 2023):
                    val_map = self.ADM2.map(self.allArea23)
                img = val_map.reduceToImage([self.feat_name],ee.Reducer.mean())
                adm_name = 'NAME_2'

            map_id = img.getMapId({
                'min': '0',
                'max': '1',
                'palette': 'A50026,B91326,DF422F,FEE695,B5DF73,006837'
            })
            obj = {
                'eeMapId': str(map_id['mapid']),
                'eeMapURL': str(map_id['tile_fetcher'].url_format),
            }
            res[feat_name] = obj
        return res

    def download_valnerabilityMap(self, type):
        # Get a download URL for the FeatureCollection.
        val_map = self.ADM3.map(self.allArea)
        url = val_map.getDownloadURL(
            filetype=type,
            selectors=["NAME_0","NAME_1","NAME_2","NAME_3", "Education0", "edu_attain0", "edu_attend0","Health0", "health_food0", "health_access0", "health_water0","health_sanit0", "health_handwash0","LivingStandard0", "liv_overcr0", "liv_hous0", "liv_cooking0", "liv_elect0", "liv_asset0", "liv_coping0","Monetary0", "overall0"],
            filename="cambodia_poverty_valnerability",
        )
        obj = {
            "downloadUrl":url,
        }
        return obj


    # 2019-------------------------------------------------------------------------
    def probabilityMaps(self, year):
        buildings = self.buildings

        if(year == 2019):
            Education = self.Education19.clip(self.ADM0)
            water = self.water19.clip(self.ADM0)
            food = self.food19.clip(self.ADM0)
            sanitation = self.sanitation19.clip(self.ADM0)
            handWashing = self.handWashing19.clip(self.ADM0)
            Health = self.Health19.clip(self.ADM0)
            overcrowding = self.overcrowding19.clip(self.ADM0)
            housing = self.housing19.clip(self.ADM0)
            fuel = self.fuel19.clip(self.ADM0)
            electricity = self.electricity19.clip(self.ADM0)
            assets = self.assets19.clip(self.ADM0)
            livelihoodBasedCopingStrategies = self.livelihoodBasedCopingStrategies19.clip(self.ADM0)
            LivingStandard = self.LivingStandard19.clip(self.ADM0)
            consumption = self.consumption19.clip(self.ADM0)
            totalV2 = self.totalV219.clip(self.ADM0)
        elif(year == 2022):
            Education = self.Education22.clip(self.ADM0)
            food = self.food22.clip(self.ADM0)
            water = self.water22.clip(self.ADM0)
            sanitation = self.sanitation22.clip(self.ADM0)
            handWashing = self.handWashing22.clip(self.ADM0)
            Health = self.Health22.clip(self.ADM0)
            overcrowding = self.overcrowding22.clip(self.ADM0)
            housing = self.housing22.clip(self.ADM0)
            fuel = self.fuel22.clip(self.ADM0)
            electricity = self.electricity22.clip(self.ADM0)
            assets = self.assets22.clip(self.ADM0)
            livelihoodBasedCopingStrategies = self.livelihoodBasedCopingStrategies22.clip(self.ADM0)
            LivingStandard = self.LivingStandard22.clip(self.ADM0)
            consumption = self.consumption22.clip(self.ADM0)
            totalV2 = self.totalV222.clip(self.ADM0)
        elif(year == 2023):
            Education = self.Education23.clip(self.ADM0)
            food = self.food23.clip(self.ADM0)
            water = self.water23.clip(self.ADM0)
            sanitation = self.sanitation23.clip(self.ADM0)
            handWashing = self.handWashing23.clip(self.ADM0)
            Health = self.Health23.clip(self.ADM0)
            overcrowding = self.overcrowding23.clip(self.ADM0)
            housing = self.housing23.clip(self.ADM0)
            fuel = self.fuel23.clip(self.ADM0)
            electricity = self.electricity23.clip(self.ADM0)
            assets = self.assets23.clip(self.ADM0)
            livelihoodBasedCopingStrategies = self.livelihoodBasedCopingStrategies23.clip(self.ADM0)
            LivingStandard = self.LivingStandard23.clip(self.ADM0)  
            consumption = self.consumption23.clip(self.ADM0)
            totalV2 = self.totalV223.clip(self.ADM0)


        all = [buildings, Education, food, water, sanitation, handWashing, Health, overcrowding, housing, fuel, electricity, assets, livelihoodBasedCopingStrategies, LivingStandard, consumption, totalV2]
        feat_id = ["prop_buildings", "prop_Education", "prop_food", "prop_water", "prop_sanitation", "prop_handWashing", "prop_Health", "prop_overcrowding", "prop_housing", "prop_fuel", "prop_electricity", "prop_assets", "prop_livelihoodBasedCopingStrategies", "prop_LivingStandard", "prop_consumption", "prop_totalV2"]
        labels = ["Buildings", "Education", "Food", "Water", "Sanitation", "Hand Washing", "Health", "Overcrowding", "Housing", "Fuel", "Electricity", "Assets", "Livelihood Based Coping", "Living Standard", "Consumption", "Overall Vulnerability"]
        res = {}
        inx =0
        for feat in all:
            map_id = feat.getMapId({
                'min': '0',
                'max': '100',
                'palette': 'darkgreen,green,yellow,orange,red,darkred'
            })
            obj = {
                'name': labels[inx],
                'eeMapId': str(map_id['mapid']),
                'eeMapURL': str(map_id['tile_fetcher'].url_format),
            }

            res[feat_id[inx]] = obj
            inx+=1
        return res
    
    
    # -------------------------------------------------------------------------
    def getTileLayerUrl(self, ee_image_object):
        map_id = ee.Image(ee_image_object).getMapId()
        tile_url_template =  str(map_id['tile_fetcher'].url_format)
        return tile_url_template

    # -------------------------------------------------------------------------
    def calLandcoverArea(self, series_start, series_end, year, area_type, area_id):
        lcImage = ee.Image( settings.LANDCOVER + str(year)).clip(self.geometry)
        classNames = ['evergreen', 'semi-evergreen', 'deciduous', 'mangrove', 'flooded forest','rubber', 'other plantations', 'rice', 'cropland', 'surface water', 'grassland', 'woodshrub', 'built-up area', 'village', 'other'];
        classNumbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        PALETTE_list = ['267300', '38A800', '70A800', '00A884', 'B4D79E','AAFF00', 'F5F57A', 'FFFFBE', 'FFD37F', '004DA8', 'D7C29E', '89CD66', 'E600A9', 'A900E6', '6f6f6f'];
        map_id = lcImage.getMapId({
            'min': '0',
            'max': str(len(classNames)-1),
            'palette': '267300, 38A800, 70A800, 00A884, B4D79E, AAFF00, F5F57A, FFFFBE, FFD37F, 004DA8, D7C29E, 89CD66, E600A9, A900E6, 6f6f6f'
        })
        return {
            # 'total_area': lcarea,
            'eeMapId': str(map_id['mapid']),
            'eeMapURL': str(map_id['tile_fetcher'].url_format),
            'color':'267300'
        }

    # -------------------------------------------------------------------------
    def getDataMap(self, start_year, end_year, area_type, area_id, data_type):
        res = {}
        for _year in range(start_year, end_year+1):
            series_start = str(_year) + '-01-01'
            series_end = str(_year) + '-12-31'
            res[str(_year)] = self.geeMap(series_start, series_end, _year, area_type, area_id, data_type)
        return res

    # -------------------------------------------------------------------------
    def getNightTimeSeriesVal(self, area_type, lon=105, lat=13.4):
        def reduce_bands(image):
            point = ee.Geometry.Point(lon, lat);
            if area_type == "sub-district":
                point = self.ADM3.filterBounds(point)
            elif area_type == "province":
                point = self.ADM1.filterBounds(point)
            elif area_type == "district":
                point = self.ADM2.filterBounds(point)
            stats = image.select(['avg_rad']).reduceRegion(ee.Reducer.mean(), point, 5000)
            return image.set(stats)

        nightlight = self.NIGHTLIGHT.map(reduce_bands)
        series = nightlight.aggregate_array('avg_rad').getInfo()
        dates = nightlight.aggregate_array('system:time_start').getInfo()
        # convert to datetime
        # dates = [datetime.datetime.fromtimestamp(d//1000.) for d in dates]
        res = []
        for i in range(len(dates)):
            item = [dates[i], series[i]]
            res.append(item)
        return res


    # -------------------------------------------------------------------------
    def getOthersMap(self, area_type, area_id):
        map_id_build = self.BUILDINGS_POP.getMapId({
            'max': '1',
            'min': '10',
            'palette': "green,yellow,orange,red,darkred,purple"
        })

        map_id_deprivation = self.DEPRIVATIONIMG.getMapId({
            'max': '1',
            'min': '10',
            'palette': "green,yellow,orange,red,darkred,purple"
        })
        return {
        "Building with Population":
            {
                'mapID': 'buildings',
                'eeMapId': str(map_id_build['mapid']),
                'eeMapURL': str(map_id_build['tile_fetcher'].url_format)
            },
        "Number of deprivations":
            {
                'mapID': 'deprivations',
                'eeMapId': str(map_id_deprivation['mapid']),
                'eeMapURL': str(map_id_deprivation['tile_fetcher'].url_format)
            },
        }



    # -------------------------------------------------------------------------
    def getLandcoverArea(self, start_year, end_year, area_type, area_id):
        res = {}
        for _year in range(start_year, end_year+1):
            series_start = str(_year) + '-01-01'
            series_end = str(_year) + '-12-31'
            res[str(_year)] = self.calLandcoverArea(series_start, series_end, _year, area_type, area_id)
        return res
