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
        # image collection
        self.LANDCOVER = ee.ImageCollection(settings.LANDCOVER)
        self.VALNERABILITY_AMD3 = ee.FeatureCollection(settings.VALNERABILITY_AMD3)
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

        #indicators
        self.buildings = ee.FeatureCollection(settings.BUILDINGS)
        self.education = ee.Image(settings.IMG_EDUCATION)
        self.school = ee.Image(settings.IMG_SCHOOL)
        self.Education = ee.Image(self.education.add(self.school)).divide(2)
        self.food = ee.Image(settings.IMG_FOOD)
        self.health = ee.Image(settings.IMG_HEALTH)
        self.water = ee.Image(settings.IMG_WATER)
        self.sanitation = ee.Image(settings.IMG_SANITATION)
        self.handWashing = ee.Image(settings.IMG_HANDWASHING)
        self.Health = ee.Image(self.food.add(self.health).add(self.water).add(self.sanitation).add(self.handWashing)).divide(5)
        self.overcrowding = ee.Image(settings.IMG_OVERCROWDING)
        self.housing = ee.Image(settings.IMG_HOUSING)
        self.fuel = ee.Image(settings.IMG_FUEL)
        self.electricity = ee.Image(settings.IMG_ELECTRICITY)
        self.assets = ee.Image(settings.IMG_ASSETS)
        self.livelihoodBasedCopingStrategies = ee.Image(settings.IMG_LIVELIHOODBASEDCOPINGSTRATEGIES)
        self.LivingStandard = ee.Image(self.overcrowding.add(self.housing).add(self.fuel).add(self.electricity).add(self.assets).add(self.livelihoodBasedCopingStrategies)).divide(6)
        self.consumption = ee.Image(settings.IMG_CONSUMPTION)
        self.totalV2 = ee.Image(settings.IMG_TOTALV2)

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
        provAll = self.VALNERABILITY_AMD3.filterBounds(prov.geometry())
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

    def valnerabilityMap(self, feat, area_type, area_id,):
        feat_names = ["Education0", "edu_attain0", "edu_attend0",
        "Health0", "health_food0", "health_access0", "health_water0","health_sanit0", "health_handwash0",
        "LivingStandard0", "liv_overcr0", "liv_hous0", "liv_cooking0", "liv_elect0", "liv_asset0", "liv_coping0",
        "Monetary0", "overall0"]
        res = {}
        adm_name = ''
        for feat_name in feat_names:
            self.feat_name = feat_name
            if area_type == "sub-district":
                val_map = self.getFraction(self.VALNERABILITY_AMD3, self.feat_name)
                img = val_map.reduceToImage(
                    properties= ["Not Deprived"],
                    reducer= ee.Reducer.mean(),
                )
                adm_name = 'NAME_3'
            elif area_type == "country":
                val_map = self.ADM0.map(self.allArea)
                img = val_map.reduceToImage([self.feat_name],ee.Reducer.mean());
                adm_name = 'NAME_0'
            elif area_type == "province":
                val_map = self.ADM1.map(self.allArea)
                img = val_map.reduceToImage([self.feat_name],ee.Reducer.mean());
                adm_name = 'NAME_1'
            elif area_type == "district":
                val_map = self.ADM2.map(self.allArea)
                img = val_map.reduceToImage([self.feat_name],ee.Reducer.mean());
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

    # -------------------------------------------------------------------------
    def probabilityMaps(self):
        buildings = self.buildings
        education = self.education
        school = self.school
        Education = self.Education
        food = self.food
        health = self.health
        water = self.water
        sanitation = self.sanitation
        handWashing = self.handWashing
        Health = self.Health
        overcrowding = self.overcrowding
        housing = self.housing
        fuel = self.fuel
        electricity = self.electricity
        assets = self.assets
        livelihoodBasedCopingStrategies = self.livelihoodBasedCopingStrategies
        LivingStandard = self.LivingStandard
        consumption = self.consumption
        totalV2 = self.totalV2

        all = [buildings, Education, food, water, sanitation, handWashing, Health, overcrowding, housing, fuel, electricity, assets, livelihoodBasedCopingStrategies, LivingStandard, consumption, totalV2]
        feat_id = ["prop_buildings", "prop_Education", "prop_food", "prop_water", "prop_sanitation", "prop_handWashing", "prop_Health", "prop_overcrowding", "prop_housing", "prop_fuel", "prop_electricity", "prop_assets", "prop_livelihoodBasedCopingStrategies", "prop_LivingStandard", "prop_consumption", "prop_totalV2"]
        labels = ["Buildings", "Education", "Food", "Water", "Sanitation", "Hand Washing", "Health", "Overcrowding", "Housing", "Fuel", "Electricity", "Assets", "Livelihood Based Coping", "Living Standard", "Consumption", "Overall Vulnerability"]
        res = {}
        inx =0
        for feat in all:
            map_id = feat.getMapId({
                'min': '20',
                'max': '80',
                'palette': '006837, B5DF73, FEE695, DF422F, B91326, A50026'
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
