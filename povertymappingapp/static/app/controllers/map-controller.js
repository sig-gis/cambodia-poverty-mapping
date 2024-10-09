(function () {

  'use strict';
  angular.module('baseApp')
    .controller('mapController', function ($scope, $http, appSettings, MapService) {

      var MAPBOXAPI = appSettings.mapboxapi;

      var map, basemap_layer, drawing_polygon;
      $scope.STUDYLOW = 2015;
      $scope.STUDYHIGH = 2020;
      var refHigh, refLow, studyHigh, studyLow;
      var arrayWMSLayers = []
      var k = 'value';
      var y = 0;
      var EVILayer, ForestGainLayer, ForestLossLayer, ForestAlertLayer;
      var overlayLayers = [EVILayer, ForestGainLayer, ForestLossLayer, ForestAlertLayer];
      var MapLayerArr = {}
      var currentSelectedArea = '';
      var pieCharts = {};


      var feat_groups = ["education", "health", "living", "monetary", "overall"];
      var feat_names = ["Education0", "edu_attain0", "edu_attend0",
        "Health0", "health_food0", "health_access0", "health_water0", "health_sanit0", "health_handwash0",
        "LivingStandard0", "liv_overcr0", "liv_hous0", "liv_cooking0", "liv_elect0", "liv_asset0", "liv_coping0",
        "Monetary0", "overall0"];

      var _groups = {
        "education": ["Education0", "edu_attain0", "edu_attend0"],
        "health": ["Health0", "health_food0", "health_access0", "health_water0", "health_sanit0", "health_handwash0",],
        "living": ["LivingStandard0", "liv_overcr0", "liv_hous0", "liv_cooking0", "liv_elect0", "liv_asset0", "liv_coping0"],
        "monetary": ["Monetary0"],
        "overall": ["overall0"],
      }
      var _feat_desc = {
        "education": ["Education", "Educational attainment", "School attendance"],
        "health": ["Health", "Food Comsumtion", "Access to Healtcare", "Access to Clean Water", "Access to Sanitation", "Hand Washing",],
        "living": ["Living Standard", "Overcrowding", "Housing Materials", "Cooking Fuel", "Access to Electricity", "Assets", "Livelihood Based Coping Strategies"],
        "monetary": ["Monetary"],
        "overall": ["overall"],
      }

      function fetchWithCache(url, storageKey, callback) {
        const cachedData = localStorage.getItem(storageKey);
        if (cachedData) {
          console.log('Serving from cache:', storageKey);
          callback(JSON.parse(cachedData));
        } else {
          $.getJSON(url, function (data) {
            console.log('Fetching from network and caching:', storageKey);
            localStorage.setItem(storageKey, JSON.stringify(data));
            callback(data);
          });
        }
      }



      function createMapVar() {
        for (y = $scope.STUDYLOW; y <= $scope.STUDYHIGH; y++) {
          eval('$scope.buildings' + y + '=null;');
          eval('$scope.deprivations' + y + '=null;');
          eval('$scope.Education0' + y + '=null;');
          eval('$scope.edu_attain0' + y + '=null;');
          eval('$scope.edu_attend0' + y + '=null;');
          eval('$scope.Health0' + y + '=null;');
          eval('$scope.health_food0' + y + '=null;');
          eval('$scope.health_access0' + y + '=null;');
          eval('$scope.health_water0' + y + '=null;');
          eval('$scope.health_sanit0' + y + '=null;');
          eval('$scope.health_handwash0' + y + '=null;');
          eval('$scope.LivingStandard0' + y + '=null;');
          eval('$scope.liv_overcr0' + y + '=null;');
          eval('$scope.liv_hous0' + y + '=null;');
          eval('$scope.liv_cooking0' + y + '=null;');
          eval('$scope.liv_elect0' + y + '=null;');
          eval('$scope.liv_asset0' + y + '=null;');
          eval('$scope.liv_coping0' + y + '=null;');
          eval('$scope.Monetary0' + y + '=null;');
          eval('$scope.overall0' + y + '=null;');
          eval('$scope.nightlight' + y + '=null;');
          eval('$scope.worldpop' + y + '=null;');
          eval('$scope.Forest' + y + '=null;');
          eval('$scope.Landcover' + y + '=null;');


          eval('$scope.prop_buildings' + y + '=null;');
          eval('$scope.prop_Education' + y + '=null;');
          eval('$scope.prop_food' + y + '=null;');
          eval('$scope.prop_water' + y + '=null;');
          eval('$scope.prop_sanitation' + y + '=null;');
          eval('$scope.prop_handWashing' + y + '=null;');
          eval('$scope.prop_Health' + y + '=null;');
          eval('$scope.prop_overcrowding' + y + '=null;');
          eval('$scope.prop_housing' + y + '=null;');
          eval('$scope.prop_fuel' + y + '=null;');
          eval('$scope.prop_livelihoodBasedCopingStrategies' + y + '=null;');
          eval('$scope.prop_LivingStandard' + y + '=null;');
          eval('$scope.prop_consumption' + y + '=null;');
          eval('$scope.prop_totalV2' + y + '=null;');

          overlayLayers.push(eval('$scope.buildings' + y));
          overlayLayers.push(eval('$scope.deprivations' + y));
          overlayLayers.push(eval('$scope.Education0' + y));
          overlayLayers.push(eval('$scope.edu_attain0' + y));
          overlayLayers.push(eval('$scope.edu_attend0' + y));
          overlayLayers.push(eval('$scope.Health0' + y));
          overlayLayers.push(eval('$scope.health_food0' + y));
          overlayLayers.push(eval('$scope.health_access0' + y));
          overlayLayers.push(eval('$scope.health_water0' + y));
          overlayLayers.push(eval('$scope.health_sanit0' + y));
          overlayLayers.push(eval('$scope.health_handwash0' + y));
          overlayLayers.push(eval('$scope.LivingStandard0' + y));
          overlayLayers.push(eval('$scope.liv_overcr0' + y));
          overlayLayers.push(eval('$scope.liv_hous0' + y));
          overlayLayers.push(eval('$scope.liv_cooking0' + y));
          overlayLayers.push(eval('$scope.liv_elect0' + y));
          overlayLayers.push(eval('$scope.liv_asset0' + y));
          overlayLayers.push(eval('$scope.liv_coping0' + y));
          overlayLayers.push(eval('$scope.Monetary0' + y));
          overlayLayers.push(eval('$scope.overall0' + y));
          overlayLayers.push(eval('$scope.nightlight' + y));
          overlayLayers.push(eval('$scope.worldpop' + y));

          overlayLayers.push(eval('$scope.prop_buildings' + y));
          overlayLayers.push(eval('$scope.prop_Education' + y));
          overlayLayers.push(eval('$scope.prop_food' + y));
          overlayLayers.push(eval('$scope.prop_water' + y));
          overlayLayers.push(eval('$scope.prop_sanitation' + y));
          overlayLayers.push(eval('$scope.prop_handWashing' + y));
          overlayLayers.push(eval('$scope.prop_Health' + y));
          overlayLayers.push(eval('$scope.prop_overcrowding' + y));
          overlayLayers.push(eval('$scope.prop_housing' + y));
          overlayLayers.push(eval('$scope.prop_fuel' + y));
          overlayLayers.push(eval('$scope.prop_livelihoodBasedCopingStrategies' + y));
          overlayLayers.push(eval('$scope.prop_LivingStandard' + y));
          overlayLayers.push(eval('$scope.prop_consumption' + y));
          overlayLayers.push(eval('$scope.prop_totalV2' + y));
          overlayLayers.push(eval('$scope.Forest' + y));
          overlayLayers.push(eval('$scope.Landcover' + y));

          MapLayerArr[y.toString()] = {
            'buildings': eval('$scope.buildings' + y),
            'deprivations': eval('$scope.deprivations' + y),
            'Education0': eval('$scope.Education0' + y),
            'edu_attain0': eval('$scope.edu_attain0' + y),
            'edu_attend0': eval('$scope.edu_attend0' + y),
            'Health0': eval('$scope.Health0' + y),
            'health_food0': eval('$scope.health_food0' + y),
            'health_access0': eval('$scope.health_access0' + y),
            'health_water0': eval('$scope.health_water0' + y),
            'health_sanit0': eval('$scope.health_sanit0' + y),
            'health_handwash0': eval('$scope.health_handwash0' + y),
            'LivingStandard0': eval('$scope.LivingStandard0' + y),
            'liv_overcr0': eval('$scope.liv_overcr0' + y),
            'liv_hous0': eval('$scope.liv_hous0' + y),
            'liv_cooking0': eval('$scope.liv_cooking0' + y),
            'liv_elect0': eval('$scope.liv_elect0' + y),
            'liv_asset0': eval('$scope.liv_asset0' + y),
            'liv_coping0': eval('$scope.liv_coping0' + y),
            'Monetary0': eval('$scope.Monetary0' + y),
            'overall0': eval('$scope.overall0' + y),
            'prop_buildings': eval('$scope.prop_buildings' + y),
            'prop_Education': eval('$scope.prop_Education' + y),
            'prop_food': eval('$scope.prop_food' + y),
            'prop_water': eval('$scope.prop_water' + y),
            'prop_sanitation': eval('$scope.prop_sanitation' + y),
            'prop_handWashing': eval('$scope.prop_handWashing' + y),
            'prop_Health': eval('$scope.prop_Health' + y),
            'prop_overcrowding': eval('$scope.prop_overcrowding' + y),
            'prop_housing': eval('$scope.prop_housing' + y),
            'prop_fuel': eval('$scope.prop_fuel' + y),
            'prop_livelihoodBasedCopingStrategies': eval('$scope.prop_livelihoodBasedCopingStrategies' + y),
            'prop_LivingStandard': eval('$scope.prop_LivingStandard' + y),
            'prop_consumption': eval('$scope.prop_consumption' + y),
            'prop_totalV2': eval('$scope.prop_totalV2' + y),
            'nightlight': eval('$scope.nightlight' + y),
            'worldpop': eval('$scope.worldpop' + y),
            'forest': eval('$scope.Forest' + y),
            'landcover': eval('$scope.Landcover' + y),
          }
        }
      }

      createMapVar();

      var selected_admin = 'Cambodia';
      //init leaflet map
      var mapCenter_lat = 12.35118782414063;
      var mapCenter_long = 104.22877523601562;
      // init map
      map = L.map('map', {
        center: [mapCenter_lat, mapCenter_long],
        zoom: 7,
        minZoom: 2,
        maxZoom: 16,
        maxBounds: [
          [-120, -220],
          [120, 220]
        ]
      });
      map.scrollWheelZoom.disable();

      ////////////////////////////////////////////////////////////////////////////////////////////////////////////

      //create the index of map overlay layers

      map.createPane('geeMapLayer');
      map.getPane('geeMapLayer').style.zIndex = 300;

      map.createPane('admin');
      map.getPane('admin').style.zIndex = 1000;
      //	map.getPane('admin').style.pointerEvents = 'none';
      map.createPane('maplayer_cam');
      map.getPane('maplayer_cam').style.zIndex = 450;
      map.getPane('maplayer_cam').style.pointerEvents = 'none';
      map.createPane('maplayer_protect');
      map.getPane('maplayer_protect').style.zIndex = 451;
      map.getPane('maplayer_protect').style.pointerEvents = 'none';

      map.createPane('maplayer_gis');
      map.getPane('maplayer_gis').style.zIndex = 1001;

      map.createPane('basemap');
      map.getPane('basemap').style.zIndex = 0;
      map.getPane('basemap').style.pointerEvents = 'none';


      basemap_layer = L.tileLayer('https://api.mapbox.com/styles/v1/servirmekong/ckduef35613el19qlsoug6u2h/tiles/256/{z}/{x}/{y}@2x?access_token=' + MAPBOXAPI, {
        attribution: '',
        pane: 'basemap'
      }).addTo(map);

      var mapWidth = map.getSize().x * 0.3;
      var mapHeight = map.getSize().y * 0.3;


      // Initialise the FeatureGroup to store editable layers
      var editableLayers = new L.FeatureGroup({ pane: 'admin' });
      map.addLayer(editableLayers);

      var drawPluginOptions = {
        draw: {
          polygon: {
            allowIntersection: false, // Restricts shapes to simple polygons
            drawError: {
              color: '#e1e100', // Color the shape will turn when intersects
              message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
            },
            shapeOptions: {
              color: '#000',
              strokeWeight: 2,
              fillOpacity: 0
            }
          },

          // disable toolbar item by setting it to false
          polyline: false,
          circle: false, // Turns off this drawing tool
          circlemarker: false,
          rectangle: {
            shapeOptions: {
              color: '#fd5a24',
              strokeWeight: 2,
              fillOpacity: 0
            }
          },
          marker: false,

        },
        edit: {
          featureGroup: editableLayers, //REQUIRED!!
          edit: true
        }
      };

      var polygonVertex = 0;


      /**
      * Add file upload button on map
      */
      var customControl = L.Control.extend({
        options: {
          position: 'topleft'
        },
        onAdd: function (map) {
          var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
          container.innerHTML = "<label for='input-file2' style='margin-left:7px;margin-top:5px;font-size:15px;cursor: pointer;' title='Load local file (Geojson, KML)'><span class='glyphicon glyphicon-folder-open' aria-hidden='true'></span><input type='file' class='hide' id='input-file2' accept='.kml,.kmz,.json,.geojson,application/json,application/vnd.google-earth.kml+xml,application/vnd.google-earth.kmz'></label>";
          container.style.backgroundColor = '#f4f4f4';
          container.style.width = '35px';
          container.style.height = '35px';
          container.style.backgroundSize = "30px 30px";
          return container;
        }
      });
      map.addControl(new customControl());


      var adm1_data = null;
      var adm2_data = null;
      var adm3_data = null;


      const static_url = "/static/";
      // $.getJSON(static_url + "data/VALNERABILITY_DATA_AMD1_v2.json", function (json) {
      //   adm1_data = json;
      //   createBarChart();
      // });

      // $.getJSON(static_url + "data/VALNERABILITY_DATA_AMD2_v2.json", function (json) {
      //   adm2_data = json;
      // });

      // $.getJSON(static_url + "data/VALNERABILITY_DATA_AMD3_v2.json", function (json) {
      //   adm3_data = json;
      // });

      fetchWithCache(static_url + "data/VALNERABILITY_DATA_AMD1_v2.json", 'adm1_data_cache', function (data) {
        adm1_data = data;
        createBarChart();
      });

      fetchWithCache(static_url + "data/VALNERABILITY_DATA_AMD2_v2.json", 'adm2_data_cache', function (data) {
        adm2_data = data;
      });

      fetchWithCache(static_url + "data/VALNERABILITY_DATA_AMD3_v2.json", 'adm3_data_cache', function (data) {
        adm3_data = data;
      });

      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      /**
       * Alert
       */
      $("#closeAlert").click(function () {
        $('.custom-alert').addClass('display-none');
        $("#alertContent").text('');
        $("#alertType").text('');
      })
      var showErrorAlert = function (alertContent) {
        $("#alertContent").text(alertContent);
        $("#alertType").text("Error! ");
        $('.custom-alert').removeClass('display-none').removeClass('alert-info').removeClass('alert-success').addClass('alert-danger');
      };

      var showSuccessAlert = function (alertContent) {
        $("#alertContent").text(alertContent);
        $("#alertType").text("Success! ");
        $('.custom-alert').removeClass('display-none').removeClass('alert-info').removeClass('alert-danger').addClass('alert-success');
      };

      var showInfoAlert = function (alertContent) {
        $("#alertContent").text(alertContent);
        $("#alertType").text("Info! ");
        $('.custom-alert').removeClass('display-none').removeClass('alert-success').removeClass('alert-danger').addClass('alert-info');
      };


      ////////////////////////////////////////////////////////////////////////////////////////////////////////////

      var mapLayer_airport = L.geoJson(airport, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, {
            radius: 5,
            fillColor: "#ff7800",
            color: "#FFF",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8,
            pane: 'maplayer_gis'
          });
        },
        onEachFeature: function (feature, layer) {
          layer.bindPopup('<pre>' + JSON.stringify(feature.properties, null, ' ').replace(/[\{\}"]/g, '') + '</pre>');
        }
      });

      var mapLayer_dams = L.geoJson(dams, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, {
            radius: 5,
            fillColor: "#294AB9",
            color: "#FFF",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8,
            pane: 'maplayer_gis'
          });
        },
        onEachFeature: function (feature, layer) {
          layer.bindPopup('<pre>' + JSON.stringify(feature.properties, null, ' ').replace(/[\{\}"]/g, '') + '</pre>');

        }
      });

      var mapLayer_main_road = L.geoJson(main_road, {
        style: function (feature) {
          return {
            color: "#C82121",
            //fill: false,
            opacity: 1,
            clickable: true,
            weight: 1,
          };
        },
        pane: 'maplayer_gis'
      });

      var mapLayer_railway = L.geoJson(railway, {
        style: function (feature) {
          return {
            color: "#E56800",
            //fill: false,
            opacity: 1,
            clickable: true,
            weight: 2,
            dashArray: 3,
          };
        },
        pane: 'maplayer_gis'
      });






      ////////////////////////////////////////////////////////////////////////////////////////////////////////////

      // Extract an array of coordinates for the given polygon.
      var getCoordinates = function (coords) {
        var polygon_coords = "";
        for (var i = 0; i < coords.length; i++) {
          if (i !== coords.length - 1) {
            polygon_coords += "(" + coords[i][1] + "," + coords[i][0] + "),";
          } else {
            polygon_coords += "(" + coords[i][1] + "," + coords[i][0] + ")";
          }
        }
        return polygon_coords;
      };

      var selected = null;
      var selected_features = [];
      var selected_layers = [];
      var previous = null;

      var LandcoverData = {}
      function highlight(layer) {
        layer.setStyle({
          weight: 5,
          dashArray: '',
          fillOpacity: 0,
          color: 'yellow'
        });
        if (!L.Browser.ie && !L.Browser.opera) {
          layer.bringToFront();
        }

      }

      function dehighlight(layer, geojson) {
        var _id = []
        if (selected_layers.length === 0) {
          geojson.resetStyle(layer);
        } else {
          selected_layers.forEach(function (selected_layer) {
            _id.push(selected_layer._leaflet_id)
          });
          if (!_id.includes(layer._leaflet_id)) {
            geojson.resetStyle(layer);
          }
        }
      }
      function select(layer, geojson, selectedArea, areaType) {
        // $scope.showLoader = true;
        if (selected !== null) {
          previous = selected;
        }
        // map.fitBounds(layer.getBounds());
        selected = layer;
        var coords = layer.feature.geometry.coordinates;
        polygon_id = getCoordinates(coords[0][0]);

        polygonVertex = coords.length;
        area_type = areaType;
        if (areaType === "province") {
          area_id = layer.feature.properties.PRO_CODE;
        } else if (areaType === "district") {
          area_id = layer.feature.properties.DIS_CODE;
        } else if (areaType === "sub-district") {
          area_id = layer.feature.properties.COM_CODE;
        } else if (areaType === "country") {
          area_id = layer.feature.properties.ID_0;
        }

        if (selected_features.includes(area_id)) {
          console.log(area_id)
        } else {
          getGraphPieData();

        }
        selected_features.push(area_id);
        highlight(selected);

        var uniqueSelected = [];
        selected_features.forEach(function (selected_feature) {
          if (uniqueSelected.indexOf(selected_feature) === -1) {
            uniqueSelected.push(selected_feature);
          }
        });
        selected_layers.push(selected);
        $('.selected_area_name').text(selectedArea);
        selected_admin = selectedArea;

      }

      function clearInfoGraphic() {
        $("#percent_deprived").text("");
        $("#no_population").text("");
        $("#no_buildings").text("");
      }

      var cam_country_layer = L.geoJson(cambodia_polygon, {
        style: function (feature) {
          return {
            color: "#222831",
            fill: false,
            opacity: 1,
            clickable: true,
            weight: 2,
          };
        },
        pane: 'admin',
      });

      var mapLayer_cam_adm1 = L.geoJson(cam_adm1, {
        style: function (feature) {
          return {
            color: "#222831",
            fill: false,
            opacity: 1,
            clickable: true,
            weight: 0.5,
          };
        },
        pane: 'maplayer_cam'
      });

      var mapLayer_cam_adm2 = L.geoJson(cam_adm2, {
        style: function (feature) {
          return {
            color: "#222831",
            fill: false,
            opacity: 1,
            clickable: true,
            weight: 0.5,
          };
        },
        pane: 'maplayer_cam'
      });

      var mapLayer_cam_adm3 = L.geoJson(cam_adm3, {
        style: function (feature) {
          return {
            color: "#222831",
            fill: false,
            opacity: 1,
            clickable: true,
            weight: 0.5,
          };
        },
        pane: 'maplayer_cam'
      });


      // mapLayer_cambodia.addTo(map);

      var cam_adm1_layer = L.geoJson(cam_adm1, {
        style: function (feature) {
          return {
            weight: 2,
            opacity: 1,
            fillOpacity: 0.1,
            color: '#333',
            dashArray: 3,
          };
        },
        onEachFeature: function (feature, layer) {
          layer.on({
            'mouseover': function (e) {
              getPopupGraphPieData(e.target.feature.properties.PRO_CODE);
              highlight(e.target);
              $(".highlight_area_textbox").css("display", "block");
              $(".highlight_area_textbox").text(e.target.feature.properties.HRName);
            },
            'mouseout': function (e) {
              // clearInfoGraphic()
              dehighlight(e.target, cam_adm1_layer);
              $(".highlight_area_textbox").css("display", "none");
            },
            'click': function (e) {
              var latlng = e.latlng;
              getNightTimeSeriesVal(latlng["lng"], latlng["lat"]);
              var selected_name = e.target.feature.properties.HRName;
              currentSelectedArea = e.target.feature.properties.HRName;
              select(e.target, cam_adm1_layer, selected_name, "province");
            }
          });
        },
        pane: 'admin',
        interactive: true
      });
      cam_adm1_layer.addTo(map);

      var cam_adm2_layer = L.geoJson(cam_adm2, {
        style: function (feature) {
          return {
            weight: 2,
            opacity: 1,
            fillOpacity: 0.1,
            color: '#333',
            dashArray: 3,
          };
        },
        onEachFeature: function (feature, layer) {
          layer.on({
            'mouseover': function (e) {
              getPopupGraphPieData(e.target.feature.properties.DIS_CODE);
              highlight(e.target);
              $(".highlight_area_textbox").css("display", "block");
              $(".highlight_area_textbox").text(e.target.feature.properties.PRO_NAME + "/" + e.target.feature.properties.DIS_NAME);
              // $(".highlight_area_textbox").text(e.target.feature.properties.DIS_NAME)
            },
            'mouseout': function (e) {
              // clearInfoGraphic();
              dehighlight(e.target, cam_adm2_layer);
              $(".highlight_area_textbox").css("display", "none");
            },
            'click': function (e) {
              var latlng = e.latlng
              getNightTimeSeriesVal(latlng["lng"], latlng["lat"]);
              var selected_name = e.target.feature.properties.DIS_NAME;
              select(e.target, cam_adm2_layer, selected_name, "district");
            }
          });

        },
        pane: 'admin',
        interactive: true
      });

      var cam_adm3_layer = L.geoJson(cam_adm3, {
        style: function (feature) {
          return {
            weight: 2,
            opacity: 1,
            fillOpacity: 0.1,
            color: '#333',
            dashArray: 3,
          };
        },
        onEachFeature: function (feature, layer) {
          layer.on({
            'mouseover': function (e) {
              getPopupGraphPieData(e.target.feature.properties.COM_CODE);
              highlight(e.target);
              $(".highlight_area_textbox").css("display", "block");
              $(".highlight_area_textbox").text(e.target.feature.properties.PRO_NAME + "/" + e.target.feature.properties.DIS_NAME + "/" + e.target.feature.properties.COM_NAME);
              // $(".highlight_area_textbox").text(e.target.feature.properties.COM_NAME);
            },
            'mouseout': function (e) {
              // clearInfoGraphic();
              dehighlight(e.target, cam_adm3_layer);
              $(".highlight_area_textbox").css("display", "none");
            },
            'click': function (e) {
              var latlng = e.latlng
              getNightTimeSeriesVal(latlng["lng"], latlng["lat"]);
              var selected_name = e.target.feature.properties.COM_NAME;
              select(e.target, cam_adm3_layer, selected_name, "sub-district");
            }
          });
        },
        pane: 'admin',
        interactive: true
      });
      // cam_adm3_layer.addTo(map);

      //init polygon first load
      var coords = cambodia_polygon.features[0].geometry.coordinates[0][0];
      var polygon_id = getCoordinates(coords);
      var area_type = 'province';
      var area_id = 'Cambodia';

      studyLow = $scope.STUDYLOW;
      studyHigh = $scope.STUDYHIGH;
      // $scope.showLoader = false;

      function getPopupGraphPieData(id) {
        var pieData = [
          { name: 'Deprived', y: 0, color: '#7CB5EC' },
          { name: 'Not Deprived', y: 0, color: '#434348' }
        ];
        var data = adm1_data;
        if (area_type === "provice") {
          data = adm1_data;
        } else if (area_type === "district") {
          data = adm2_data;
        } else if (area_type === "sub-district") {
          data = adm3_data;
        }
        var index = data["id_area"].indexOf(id);
        var feat = "overall0"
        var _featData = data[feat];
        var percent_dep = (_featData["Deprived"][index] * 100).toFixed(2);
        var categorical_deprived = "";

        // Get the current full URL
        var currentUrl = window.location.href;

        // Use regex to extract the language code from the URL
        var langCode = currentUrl.match(/\/(en|kh)\//);

        // Check if the match is found
        if (langCode[1] === 'kh') {
          if (percent_dep <= 20) {
            categorical_deprived = "ទាបខ្លាំង";
          } else if (percent_dep <= 40) {
            categorical_deprived = "ទាប";
          } else if (percent_dep <= 60) {
            categorical_deprived = "មធ្យម";
          } else if (percent_dep <= 80) {
            categorical_deprived = "ខ្ពស់";
          } else if (percent_dep <= 100) {
            categorical_deprived = "ខ្ពស់ខ្លាំង";
          }
        } else {
          if (percent_dep <= 20) {
            categorical_deprived = "Very low";
          } else if (percent_dep <= 40) {
            categorical_deprived = "Low";
          } else if (percent_dep <= 60) {
            categorical_deprived = "Medium";
          } else if (percent_dep <= 80) {
            categorical_deprived = "High";
          } else if (percent_dep <= 100) {
            categorical_deprived = "Very high";
          }
        }
        
        $("#no_population").text(parseInt(data["population"][index]));
        $("#no_buildings").text(parseInt(data["buildings"][index]));
        $(".info_areaname").text(data["name_area"][index]);
        $("#categorical_deprived").text(categorical_deprived);
        // $("#categorical_deprived").text(categorical_deprived)
        $("#categorical_deprived").append('<span style="font-size: 14px;"> (' + percent_dep + '%)</span>')

      }


      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      function download(url, filename) {
        fetch(url).then(function (t) {
          return t.blob().then((b) => {
            var a = document.createElement("a");
            a.href = URL.createObjectURL(b);
            a.setAttribute("download", filename);
            a.click();
            $scope.showLoader = false;
          }
          );
        });
      }
      function downloadMetadata(url, filename) {
        fetch(url).then(function (t) {
          return t.blob().then((b) => {
            var a = document.createElement("a");
            a.href = URL.createObjectURL(b);
            a.setAttribute("download", filename);
            a.click();
            $scope.showLoader = false;
          }
          );
        });
      }


      function createToggleList(parentUL, inputID, label, yid, checked, bgcolor) {
        // Get the current full URL
        var currentUrl = window.location.href;
        // Use regex to extract the language code from the URL
        var langCode = currentUrl.match(/\/(en|kh)\//);
        var activeLang = langCode[1];
        var labels = {
          'en': {
            'Education': 'Education',
            'Educational attainment': 'Educational attainment',
            'School attendance': 'School attendance',
            'Health': 'Health',
            'Food Comsumtion': 'Food Comsumtion',
            'Access to Healtcare': 'Access to Healtcare',
            'Access to Clean Water': 'Access to Clean Water',
            'Access to Sanitation': 'Access to Sanitation',
            'Hand Washing': 'Hand Washing',
            'Living Standard': 'Living Standard',
            'Overcrowding': 'Overcrowding',
            'Housing Materials': 'Housing Materials',
            'Access to Electricity': 'Access to Electricity',
            'Assets': 'Assets',
            'Livelihood Based Coping Strategies': 'Livelihood Based Coping Strategies',
            'Monetary': 'Monetary',
            'overall': 'overall'
          }, 
         'kh': {
            'Education': 'អប់រំ',
            'Educational attainment': 'ទទួលបានការអប់រំ',
            'School attendance': 'ចូលរៀននៅសាលា',
            'Health': 'សុខភាព',
            'Food Comsumtion': 'ការហូបចុក',
            'Access to Healtcare': 'ការទទួលបានសេវាសុខាភិបាល',
            'Access to Clean Water': 'ការទទួលបានទឹកស្អាត',
            'Access to Sanitation': 'ការទទួលបានអនាម័យ',
            'Hand Washing': 'ការលាងសម្អាតដៃ',
            'Living Standard': 'ស្តង់ដាររស់នៅ',
            'Overcrowding': 'ការរស់នៅដោយចង្អៀត',
            'Housing Materials': 'សម្ភារៈលំនៅដ្ឋាន',
            'Access to Electricity': 'ទទួលបានប្រើអគ្គិសនី',
            'Assets': 'ទ្រព្យសម្បត្តិ',
            'Livelihood Based Coping Strategies': 'យុទ្ធសាស្ត្រដោះស្រាយកង្វះខាតជីវភាព',
            'Monetary': 'ស្តង់ដាររស់នៅ',
            'overall': 'សរុប'
         }
        }
        $("#" + parentUL).append(
          '<li class="toggle">' +
          '<label class="switch_layer"><input name="' + inputID + '" id="' + inputID + '" data-id="' + inputID + '"  data-yid="' + yid + '" data-name="' + label + '" data-color="#' + bgcolor + '" type="checkbox" ' + checked + '><span class="slider_toggle round"></span></input></label><label>' + labels[activeLang][label] + '</label></li>'
        );
      }

      function createSelectedAreaReport(parentUL, data, area_name, area_id, chartType) {
        if (chartType === "pie") {
          $("#" + parentUL).append(
            '<div class="col-lg-12">' +
            '<p>' + area_name + '</p>' +
            '<div class="row">' +
            '<div class="col-lg-12">' +
            '<a id="' + data + '_piepng" data-yid="' + data + '" class="chart-btn-sm">PNG</a>' +
            '<a id="' + data + '_piecsv" data-yid="' + data + '" class="chart-btn-sm">CSV</a>' +
            '<div id="' + data + '_piechart"  width="1000" height="1000" style="border: 0px solid #eee;margin-bottom:15px;margin-top:5px;"></div>' +
            '</div>' +
            '</div>' +
            '</div>'
          );
        } else {
          $("#" + parentUL).append(
            '<div class="col-lg-12">' +
            '<div class="row">' +
            '<div class="col-lg-12">' +
            // '<p>Summary of '+data+' from '+ $scope.STUDYLOW +' to '+ $scope.STUDYHIGH +' </p>'+
            '<a id="' + data + '_barpng" data-yid="' + data + '" class="chart-btn-sm">PNG</a>' +
            '<a id="' + data + '_barcsv" data-yid="' + data + '" class="chart-btn-sm">CSV</a>' +
            '<div id="' + data + '_barchart"  width="1000" height="1000" style="border: 0px solid #eee;margin-bottom:15px;margin-top:5px;"></div>' +
            '</div>' +
            '</div>' +
            '</div>'
          );
        }
      }

      // function to add and update tile layer to map
      function addMapLayer(layer, url, pane) {
        layer = L.tileLayer(url, {
          attribution: '<a href="https://earthengine.google.com" target="_">' +
            'Google Earth Engine</a>;',
          pane: pane
        });
        return layer;
      }


      function showPieHighChart(chartContainer, chartSeries, subtitle, featname) {// Data retrieved from https://olympics.com/en/olympic-games/beijing-2022/medals
        // Highcharts.chart(chartContainer, {
        //     chart: {
        //         type: 'pie',
        //         options3d: {
        //             enabled: true,
        //             alpha: 0
        //         },
        //         width: 410,
        // 				height: 200,
        // 				style: {
        // 					fontFamily: "Roboto Condensed"
        // 				},
        //     },
        //     tooltip: {
        // 			formatter: function () {
        // 				return this.point.name + " (" + this.point.percentage.toFixed(2) + "%)";
        // 			}
        // 			// pointFormat: '{series.name}: <br>{point.percentage:.1f} %<br>: {point.total}'
        // 		},
        //     title: false,
        //     subtitle: subtitle,
        //     plotOptions: {
        //         pie: {
        //             innerSize: 100,
        //             depth: 45
        //         }
        //     },
        //     series: [{
        //         name: 'Deprivation',
        //         data: chartSeries
        //     }]
        // });

        Highcharts.chart(chartContainer, {
          chart: {
            type: 'pie',
            // Explicitly tell the width and height of a chart
            width: 410,
            height: 200,
            style: {
              fontFamily: "Roboto Condensed"
            },
            renderTo: chartContainer
          },
          credits: {
            enabled: false
          },
          tooltip: {
            formatter: function () {
              return this.point.name + " (" + this.point.percentage.toFixed(2) + "%)";
            }
            // pointFormat: '{series.name}: <br>{point.percentage:.1f} %<br>: {point.total}'
          },

          title: false,
          subtitle: subtitle,

          exporting: {
            chartOptions: {
              title: {
                text: ''
              },
              subtitle: {
                text: subtitle //subtitle
              }
            },
            enabled: false
          },

          credits: {
            enabled: false
          },
          plotOptions: {
            pie: {
              allowPointSelect: false,
              cursor: 'pointer',
              dataLabels: {
                enabled: false,
                format: '',
                style: { fontFamily: 'Roboto Condensed' }
              },
              showInLegend: true,
            }

          },
          legend: {
            layout: 'horizontal',
            align: 'left',
            verticalAlign: 'bottom',
            itemMarginTop: 3,
            itemMarginBottom: 3,
            itemStyle: {
              color: '#666666',
              fontWeight: 'normal',
              fontSize: '9px'
            },
            labelFormatter: function () {
              return this.name + " (" + this.percentage.toFixed(2) + "%)";
            }
          },
          series: [{
            innerSize: '50%',
            data: chartSeries
          }],
        });


      }


      function showHighChart(chartContainer, chartType, categories, chartSeries, labelArea, pointWidth, subtitle) {

        Highcharts.chart(chartContainer, {
          chart: {
            type: chartType,
            style: {
              fontFamily: 'Roboto Condensed'
            },
            width: 410,
            height: 200,
          },
          title: false,
          subtitle: subtitle,
          xAxis: {
            categories: categories,
            // crosshair: true,
            labels: {
              rotation: -45
            }
          },
          yAxis: {
            title: {
              text: null
            },
            min: 0,
            max: 1,
            labels: {
              formatter: function () {
                if (labelArea) {
                  return (this.value);
                } else {
                  return (this.value);
                }
              }
            }
          },
          exporting: {
            chartOptions: {
              title: {
                text: ''
              },
              subtitle: {
                text: subtitle
              }
            },
            enabled: false
          },
          credits: {
            enabled: false
          },
          tooltip: {
            formatter: function () {
              if (labelArea) {
                return this.series.name + " (" + this.point.y + " )";
              } else {
                return this.series.name + " (" + this.point.y + " )";
              }
            }
          },
          plotOptions: {
            // column: {
            // 	pointPadding: 0.1,
            // 	pointWidth: 20,
            // 	borderWidth: 0
            // },
            series: {
              stacking: 'normal',
              // pointWidth: 15
            },
            // bar: {
            // 	pointWidth: 10,
            // }
          },
          series: chartSeries,
          legend: {
            layout: 'horizontal',
            align: 'left',
            verticalAlign: 'bottom',
            itemMarginTop: 3,
            itemMarginBottom: 3,
            itemStyle: {
              color: '#666666',
              fontWeight: 'normal',
              fontSize: '9px'
            }
          },
        });

      }


      function showColHightChart(chartContainer, chartType, categories, chartSeries, labelArea, pointWidth, subtitle) {

        Highcharts.chart(chartContainer, {
          chart: {
            type: chartType,
            style: {
              fontFamily: 'Roboto Condensed',
              fontSize: 10
            },
            width: 410,
            height: 200,
          },
          title: false,
          subtitle: false,
          xAxis: {
            categories: categories,
            // crosshair: true,
            labels: {
              rotation: -90
            }
          },
          yAxis: {
            title: {
              text: null
            },
            min: 0,
            max: 1,
            labels: {
              formatter: function () {
                if (labelArea) {
                  return (this.value);
                } else {
                  return (this.value);
                }
              }
            }
          },
          exporting: {
            chartOptions: {
              title: {
                text: ''
              },
              subtitle: {
                text: subtitle
              }
            },
            enabled: false
          },
          credits: {
            enabled: false
          },
          tooltip: {
            formatter: function () {
              if (labelArea) {
                return this.series.name + " (" + this.point.y + " )";
              } else {
                return this.series.name + " (" + this.point.y + " )";
              }
            }
          },
          plotOptions: {},
          series: chartSeries,
          legend: true,
        });

      }


      function cal() {
        $("#toggle-list-forest").html('');
        $("#toggle-list-evi").html('');
        $("#toggle-list-forest-alert").html('');
        $("#toggle-list-sar-alert").html('');
        $("#toggle-list-burned-area").html('');
        $("#toggle-list-landcover").html('');

        //show spiner
        $scope.showLoader = true;
        getDataMap('HEALTH');
        getDataMap('ASSETS');
        getDataMap('FUEL');
        getDataMap('EDUCATION');
        getDataMap('FOOD');
        getDataMap('HOUSING');
        getDataMap('SCHOOL');
        getDataMap('ELECTRICITY');
        getDataMap('WATER');
        getDataMap('SANITATION');


      }

      var forestAreaEndYear = 0;
      function getForestMapID() {
        var parameters = {
          polygon_id: polygon_id,
          treeCanopyDefinition: 10,
          treeHeightDefinition: 5,
          startYear: studyLow,
          endYear: studyHigh,
          type: 'forestExtend',
          area_id: area_id,
          area_type: area_type,
          download: false
        };

        MapService.getForestMapID(parameters)
          .then(function (res) {
            var data = res;
            var forestArea = [];
            var noneforestArea = [];
            var yearArr = [];

            for (var i = studyLow; i <= studyHigh; i++) {
              //create map layer index
              var year_string = i.toString();
              yearArr.push(year_string);


              if (map.hasLayer(MapLayerArr[year_string].forest)) {
                map.removeLayer(MapLayerArr[year_string].forest);
              }
              //add map layer
              MapLayerArr[year_string].forest = addMapLayer(MapLayerArr[year_string].forest, data[year_string].eeMapURL, 'geeMapLayer');
              //set map style with opacity = 0.5
              MapLayerArr[year_string].forest.setOpacity(1);

              /*jshint loopfunc: true */
              createToggleList('toggle-list-forest', 'forest_' + year_string, year_string, year_string, '', data[year_string].color);


              //toggle each of forest map layer
              $("#forest_" + year_string).change(function () {
                var layerID = $(this).attr('data-yid');
                var toggleColor = $(this).attr('data-color');
                var toggleName = $(this).attr('data-name');
                var toggleId = $(this).attr('data-id');
                if (this.checked) {
                  $(this).closest("label").find("span").css("background-color", toggleColor);
                  $("#ul-forest-legend").append(
                    '<li id="' + toggleId + '"> <p><span style="width: 500px; height: 100px; background:' + toggleColor + '; border: 1px solid ' + toggleColor + '; color:' + toggleColor + '; "> XX</span> ' + toggleName + '</p> </li>'
                  );
                  MapLayerArr[layerID].forest.addTo(map);
                } else {
                  $(this).closest("label").find("span").css("background-color", '#bbb');
                  if (map.hasLayer(MapLayerArr[layerID].forest)) {
                    map.removeLayer(MapLayerArr[layerID].forest);
                  }
                  $('li[id="' + toggleId + '"').remove();
                }
              });

            }


          }, function (error) {
            console.log(error);
          });
      }
      // getForestMapID();
      var timeSeriesArr = [];
      function getNightTimeSeriesVal(lon, lat) {
        var parameters = {
          area_type: area_type,
          lon: lon,
          lat: lat,
        };
        MapService.getNightTimeSeriesVal(parameters)
          .then(function (data) {
            timeSeriesArr.push({
              type: 'area',
              name: selected_admin,
              data: data
            });
            Highcharts.chart('nightlight_linechart', {
              chart: {
                zoomType: 'x',
                style: {
                  fontFamily: "Roboto Condensed"
                },
              },
              title: {
                text: ''
              },
              subtitle: {
                enabled: false
              },
              xAxis: {
                type: 'datetime'
              },
              yAxis: {
                title: {
                  text: 'Band Value'
                }
              },
              legend: {
                enabled: true
              },
              credits: {
                enabled: false
              },
              exporting: {
                chartOptions: {
                  title: {
                    text: ''
                  },
                  subtitle: {
                    text: "Nightlight time series"
                  }
                },
                enabled: false
              },
              plotOptions: {
                area: {
                  fillColor: {
                    linearGradient: {
                      x1: 0,
                      y1: 0,
                      x2: 0,
                      y2: 1
                    },
                    stops: [
                      [0, Highcharts.getOptions().colors[0]],
                      [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                  },
                  marker: {
                    radius: 2
                  },
                  lineWidth: 1,
                  states: {
                    hover: {
                      lineWidth: 1
                    }
                  },
                  threshold: null
                }
              },
              series: timeSeriesArr
            });

            $("#nightlight-div").css("display", "block");


            $("#nightlight_line_png").click(function () {
              var nightlight_linechart = $("#nightlight_linechart").highcharts();
              nightlight_linechart.exportChart();
            });
            $("#nightlight_line_csv").click(function () {
              var nightlight_linechart = $("#nightlight_linechart").highcharts();
              nightlight_linechart.downloadCSV();
            });

          }, function (error) {
            console.log(error);
          });
      }

      function getNightLightMap() {
        // $scope.showLoader = true;
        var parameters = {
          startYear: 2015,
          endYear: 2021,
          area_type: area_type,
          area_id: area_id,
        };
        var area_data = [];
        var _yearArr = [];

        MapService.getNightLightMap(parameters)
          .then(function (data) {
            for (var i = studyLow; i <= studyHigh; i++) {
              var _yearData = data[i.toString()];
              var _year = i.toString();
              var item = data[_year];
              var keys = [];
              for (var key in item) {
                if (item.hasOwnProperty(key)) {
                  var _data = item[key]
                  //add map layer
                  MapLayerArr[_year][_data["mapID"]] = addMapLayer(MapLayerArr[_year][_data["mapID"]], _data.eeMapURL, 'geeMapLayer');
                  createToggleList('toggle-list-' + _data["mapID"], _data["mapID"] + _year, _year, _data["mapID"], '', '333'); //parentUL, inputID, label, yid, checked, bgcolor
                  //toggle each of forest map layer
                  $('#' + _data["mapID"] + _year).change(function () {
                    var layerID = $(this).attr('data-yid');
                    var yearData = $(this).attr('data-name');
                    if (this.checked) {
                      var toggleColor = $(this).attr('data-color');
                      $(this).closest("label").find("span").css("background-color", toggleColor);
                      MapLayerArr[yearData][layerID].setOpacity(1);
                      MapLayerArr[yearData][layerID].addTo(map);

                    } else {
                      $(this).closest("label").find("span").css("background-color", '#bbb');
                      if (map.hasLayer(MapLayerArr[yearData][layerID])) {
                        map.removeLayer(MapLayerArr[yearData][layerID]);
                      }
                    }
                  });
                }
              }
            }
          }, function (error) {
            console.log(error);
          });
      }
      getNightLightMap();


      function getPropMap() {
        // $scope.showLoader = true;
        var parameters = {
          area_type: area_type,
          area_id: area_id,
        };
        var area_data = [];
        var _yearArr = [];

        MapService.getPropMap(parameters)
          .then(function (data) {

            var _keys = Object.keys(data);
            for (var i = 0; i < _keys.length; i++) {
              var _featData = data[_keys[i]];
              //add map layer
              MapLayerArr[2020][_keys[i]] = addMapLayer(MapLayerArr[2020][_keys[i]], _featData.eeMapURL, 'geeMapLayer');
              /*jshint loopfunc: true */
              if (_keys[i] === "prop_totalV2") {
                // createToggleList('toggle-list-probability', _keys[i], _featData.name, 2020, 'checked', '333');
                MapLayerArr[2020].prop_totalV2.setOpacity(1);
                MapLayerArr[2020].prop_totalV2.addTo(map);
              } else {
                // createToggleList('toggle-list-probability', _keys[i], _featData.name, 2020, '', '333');
              }
              //toggle each of forest map layer
              $('#' + _keys[i]).change(function () {
                var layerID = $(this).attr('data-yid');
                var dataID = $(this).attr('data-id');
                if (this.checked) {
                  var toggleColor = $(this).attr('data-color');
                  $(this).closest("label").find("span").css("background-color", toggleColor);
                  MapLayerArr[layerID][dataID].setOpacity(1);
                  MapLayerArr[layerID][dataID].addTo(map);

                } else {
                  $(this).closest("label").find("span").css("background-color", '#bbb');
                  if (map.hasLayer(MapLayerArr[layerID][dataID])) {
                    map.removeLayer(MapLayerArr[layerID][dataID]);
                  }
                }
              });
            }
            $scope.showLoader = false;
          }, function (error) {
            console.log(error);
          });
      }

      getPropMap();


      function createBarChart() {
        var data = adm1_data;
        if (area_type === "provice") {
          data = adm1_data;
        } else if (area_type === "district") {
          data = adm2_data;
        } else if (area_type === "sub-district") {
          data = adm3_data;
        }
        for (var j = 0; j < feat_groups.length; j++) {
          var _listFeat = _groups[feat_groups[j]];
          var _listFeatDesc = _feat_desc[feat_groups[j]];
          for (var i = 0; i < _listFeat.length; i++) {

            var feat = _listFeat[i]

            var _featData = data[feat];
            var colChartSeries = [{
              "name": "Deprivation",//_listFeatDesc[i],
              "data": _featData["Deprived"],
              "color": "#0468b1"
            }]
            showColHightChart(feat.toLowerCase() + '_barchart_adm', 'column', data["name_area"], colChartSeries, true, 5, 'OVERALL DEPRIVATION BY ADMINISTRATIVE LEVEL');
          }
        }

      }
      // createBarChart();
      function getMapVal() {
        $scope.showLoader = true;
        var parameters = {
          feat: "overall0",
          area_type: area_type,
          area_id: area_id,
        };
        var area_data = [];
        var _yearArr = [];

        var lcclass = [
          { name: 'Deprived', data: [], color: '#7CB5EC' },
          { name: 'Not Deprived', data: [], color: '#434348' },
        ];
        var pieData = [
          { name: 'Deprived', y: 0, color: '#7CB5EC' },
          { name: 'Not Deprived', y: 0, color: '#434348' }
        ];

        MapService.getMapVal(parameters)
          .then(function (data) {

            var feat_groups = ["education", "health", "living", "monetary", "overall"];
            var colNames = [];

            for (var j = 0; j < feat_groups.length; j++) {
              var _listFeat = _groups[feat_groups[j]];
              var _listFeatDesc = _feat_desc[feat_groups[j]];
              for (var i = 0; i < _listFeat.length; i++) {
                var _year = 2020;
                var feat = _listFeat[i]
                colNames.push(_listFeatDesc[i]);
                var _featData = data[feat];
                if (map.hasLayer(MapLayerArr[_year][feat])) {
                  map.removeLayer(MapLayerArr[_year][feat]);
                }
                //add map layer
                MapLayerArr[_year][feat] = addMapLayer(MapLayerArr[_year][feat], _featData.eeMapURL, 'geeMapLayer');
                /*jshint loopfunc: true */
                createToggleList('toggle-list-' + feat_groups[j], feat, _listFeatDesc[i], _year, '', '333');
                //toggle each of forest map layer
                $('#' + feat).change(function () {
                  var layerID = $(this).attr('data-yid');
                  var dataName = $(this).attr('data-id');
                  if (this.checked) {
                    var toggleColor = $(this).attr('data-color');
                    $(this).closest("label").find("span").css("background-color", toggleColor);
                    MapLayerArr[layerID][dataName].setOpacity(1);
                    MapLayerArr[layerID][dataName].addTo(map);

                  } else {
                    $(this).closest("label").find("span").css("background-color", '#bbb');
                    if (map.hasLayer(MapLayerArr[layerID][dataName])) {
                      map.removeLayer(MapLayerArr[layerID][dataName]);
                    }
                  }
                });
              }
            }

            $scope.showLoader = false;

          }, function (error) {
            console.log(error);
          });
      }

      getMapVal();

      var _focusedAreas = [];
      var _barChartInfo = {
        "Education0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "edu_attain0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "edu_attend0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "Health0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "health_food0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "health_access0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "health_water0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "health_sanit0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "health_handwash0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "LivingStandard0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "liv_overcr0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "liv_hous0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "liv_cooking0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "liv_elect0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "liv_asset0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "liv_coping0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "Monetary0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
        "overall0": [
          { name: 'Not Deprived', data: [], color: '#434348' },
          { name: 'Deprived', data: [], color: '#7CB5EC' },
        ],
      }
      function getGraphPieData() {
        // $scope.showLoader = true;
        var parameters = {
          feat: "overall0",
          area_type: area_type,
          area_id: area_id,
        };
        var area_data = [];
        var _yearArr = [];
        var lcclass = [
          { name: 'Deprived', data: [], color: '#7CB5EC' },
          { name: 'Not Deprived', data: [], color: '#434348' },
        ];

        $("#health0_chart_report_area").html("");
        $("#health_access0_chart_report_area").html("");
        $("#health_water0_chart_report_area").html("");
        $("#health_sanit0_chart_report_area").html("");
        $("#health_food0_chart_report_area").html("");
        $("#health_handwash0_chart_report_area").html("");
        $("#education0_chart_report_area").html("");
        $("#edu_attain0_chart_report_area").html("");
        $("#edu_attend0_chart_report_area").html("");

        $("#livingstandard0_chart_report_area").html("");
        $("#liv_overcr0_chart_report_area").html("");
        $("#liv_hous0_chart_report_area").html("");
        $("#liv_cooking0_chart_report_area").html("");
        $("#liv_asset0_chart_report_area").html("");
        $("#liv_coping0_chart_report_area").html("");
        $("#liv_elect0_chart_report_area").html("");

        $("#monetary0_chart_report_area").html("");
        $("#overall0_chart_report_area").html("");

        const static_url = "/static/";
        var _jsonfile = static_url + "data/VALNERABILITY_DATA_AMD1_v2.json";
        if (area_type === "provice") {
          _jsonfile = static_url + "data/VALNERABILITY_DATA_AMD1_v2.json";
        } else if (area_type === "district") {
          _jsonfile = static_url + "data/VALNERABILITY_DATA_AMD2_v2.json";
        } else if (area_type === "sub-district") {
          _jsonfile = static_url + "data/VALNERABILITY_DATA_AMD3_v2.json";
        }

        $.getJSON(_jsonfile, function (json) {
          var data = json;
          var index = data["id_area"].indexOf(area_id);
          index = parseInt(index);
          var feat_groups = ["education", "health", "living", "monetary", "overall"];
          var feat_names = ["Education0", "edu_attain0", "edu_attend0",
            "Health0", "health_food0", "health_access0", "health_water0", "health_sanit0", "health_handwash0",
            "LivingStandard0", "liv_overcr0", "liv_hous0", "liv_cooking0", "liv_elect0", "liv_asset0", "liv_coping0",
            "Monetary0", "overall0"];

          var _groups = {
            "education": ["Education0", "edu_attain0", "edu_attend0"],
            "health": ["Health0", "health_food0", "health_access0", "health_water0", "health_sanit0", "health_handwash0",],
            "living": ["LivingStandard0", "liv_overcr0", "liv_hous0", "liv_cooking0", "liv_elect0", "liv_asset0", "liv_coping0"],
            "monetary": ["Monetary0"],
            "overall": ["overall0"],
          }
          var _feat_desc = {
            "education": ["Education", "Educational attainment", "School attendance"],
            "health": ["Health", "Food Comsumtion", "Access to Healtcare", "Access to Clean Water", "Access to Sanitation", "Hand Washing",],
            "living": ["Living Standard", "Overcrowding", "Housing Materials", "Cooking Fuel", "Access to Electricity", "Assets", "Livelihood Based Coping Strategies"],
            "monetary": ["Monetary"],
            "overall": ["overall"],
          }
          _focusedAreas.push(selected_admin);

          for (var j = 0; j < feat_groups.length; j++) {
            var _listFeat = _groups[feat_groups[j]];
            var _listFeatDesc = _feat_desc[feat_groups[j]];
            for (var i = 0; i < _listFeat.length; i++) {

              var _year = 2020;
              var feat = _listFeat[i]
              var feat_des = _listFeatDesc[i]

              var _featData = data[feat];
              var pieData = [];
              pieData.push(["Deprived", _featData["Deprived"][index], '#7CB5EC']);
              pieData.push(["Not Deprived", _featData["Not Deprived"][index], '#434348']);

              _barChartInfo[feat][0]["data"].push(_featData["Not Deprived"][index]);
              _barChartInfo[feat][1]["data"].push(_featData["Deprived"][index]);
              var report_div_id = feat.toLowerCase() + "_chart_report_area";

              if (_focusedAreas.length > 1) {
                createSelectedAreaReport(report_div_id, feat.toLowerCase(), selected_admin, area_id, "bar");
                var barChartID = feat.toLowerCase() + '_barchart';
                showHighChart(barChartID, 'column', _focusedAreas, _barChartInfo[feat], true, 5, feat_des.toUpperCase());
                $("#" + feat.toLowerCase() + "_barpng").click(function () {
                  var dataName = $(this).attr('data-yid');
                  var chart = $("#" + dataName.toLowerCase() + '_barchart').highcharts();
                  chart.exportChart();
                });
                $("#" + feat.toLowerCase() + "_barcsv").click(function () {
                  var dataName = $(this).attr('data-yid');
                  var chart = $("#" + dataName.toLowerCase() + '_barchart').highcharts();
                  chart.downloadCSV();
                });

              } else {
                createSelectedAreaReport(report_div_id, feat.toLowerCase(), selected_admin, area_id, "pie");
                var pieChartID = feat.toLowerCase() + '_piechart';
                showPieHighChart(pieChartID, pieData, feat_des.toUpperCase() + ' IN ' + selected_admin.toUpperCase(), feat.toLowerCase());
                // A $( document ).ready() block.
                $("#" + feat.toLowerCase() + "_piepng").click(function () {
                  var dataName = $(this).attr('data-yid');
                  var chart = $("#" + dataName.toLowerCase() + '_piechart').highcharts();
                  chart.exportChart();
                });

                $("#" + feat.toLowerCase() + "_piecsv").click(function () {
                  var dataName = $(this).attr('data-yid');
                  var chart = $("#" + dataName.toLowerCase() + '_piechart').highcharts();
                  chart.downloadCSV();
                });
              }

            }
          }
        });


      }

      function getOthersMap() {
        var parameters = {
          area_type: area_type,
          area_id: area_id,
        };
        var area_data = [];
        var _yearArr = [];

        MapService.getOthersMap(parameters)
          .then(function (data) {
            var keys = [];
            for (var key in data) {
              if (data.hasOwnProperty(key)) {
                keys.push(key);
                var _data = data[key]
                //add map layer
                MapLayerArr[studyHigh][_data["mapID"]] = addMapLayer(MapLayerArr[studyHigh][_data["mapID"]], _data.eeMapURL, 'geeMapLayer');
                createToggleList('toggle-list-others', _data["mapID"], key, '', '', '333');
                //toggle each of forest map layer
                $('#' + _data["mapID"]).change(function () {
                  var dataName = $(this).attr('data-id');
                  if (this.checked) {
                    var toggleColor = $(this).attr('data-color');
                    $(this).closest("label").find("span").css("background-color", toggleColor);
                    MapLayerArr[studyHigh][dataName].setOpacity(1);
                    MapLayerArr[studyHigh][dataName].addTo(map);

                  } else {
                    $(this).closest("label").find("span").css("background-color", '#bbb');
                    if (map.hasLayer(MapLayerArr[studyHigh][dataName])) {
                      map.removeLayer(MapLayerArr[studyHigh][dataName]);
                    }
                  }
                });

              }
            }
          }, function (error) {
            console.log(error);
          });
      }

      getOthersMap();


      function getDataMap(data_type) {
        var parameters = {
          area_type: area_type,
          area_id: area_id,
          data: data_type,
          polygon_id: polygon_id,
          startYear: studyLow,
          endYear: studyHigh,
          data: data_type
        };
        var area_data = [];
        var _yearArr = [];

        MapService.getMapData(parameters)
          .then(function (data) {
            for (var i = studyLow; i <= studyHigh; i++) {
              var _yearData = data[i.toString()];
              var _year = i.toString();
              MapLayerArr[_year][data_type] = addMapLayer(MapLayerArr[_year][data_type], _yearData.eeMapURL, 'geeMapLayer');
              createToggleList('toggle-list-' + data_type.toLowerCase(), area_id + data_type + _year, _year, _year, '', '333');

              //toggle each of forest map layer
              $('#' + area_id + data_type + _year).change(function () {
                var layerID = $(this).attr('data-yid');
                if (this.checked) {
                  var toggleColor = $(this).attr('data-color');
                  $(this).closest("label").find("span").css("background-color", toggleColor);
                  MapLayerArr[layerID][data_type].setOpacity(1);
                  MapLayerArr[layerID][data_type].addTo(map);

                } else {
                  $(this).closest("label").find("span").css("background-color", '#bbb');
                  if (map.hasLayer(MapLayerArr[layerID][data_type])) {
                    map.removeLayer(MapLayerArr[layerID][data_type]);
                  }
                }
              });
            }
            $scope.showLoader = false;
          }, function (error) {
            console.log(error);
          });
      }

      function getLandcover() {
        var parameters = {
          polygon_id: polygon_id,
          startYear: studyLow,
          endYear: studyHigh,
          area_type: area_type,
          area_id: area_id,
          year: '',
          download: false
        };
        var area_data = [];
        var _yearArr = [];
        var lcclass = [
          { name: 'evergreen', data: [], color: '#434348' },
          { name: 'semi-evergreen', data: [], color: '#38A800' },
          { name: 'deciduous', data: [], color: '#70A800' },
          { name: 'mangrove', data: [], color: '#00A884' },
          { name: 'flooded forest', data: [], color: '#B4D79E' },
          { name: 'rubber', data: [], color: '#AAFF00' },
          { name: 'other plantations', data: [], color: '#F5F57A' },
          { name: 'rice', data: [], color: '#FFFFBE' },
          { name: 'cropland', data: [], color: '#FFD37F' },
          { name: 'surface water', data: [], color: '#004DA8' },
          { name: 'grassland', data: [], color: '#D7C29E' },
          { name: 'woodshrub', data: [], color: '#89CD66' },
          { name: 'built-up area', data: [], color: '#E600A9' },
          { name: 'village', data: [], color: '#A900E6' },
          { name: 'other', data: [], color: '#6f6f6f' }
        ];
        var pieData = [
          { name: 'evergreen', y: 0, color: '#434348' },
          { name: 'semi-evergreen', y: 0, color: '#38A800' },
          { name: 'deciduous', y: 0, color: '#70A800' },
          { name: 'mangrove', y: 0, color: '#00A884' },
          { name: 'flooded forest', y: 0, color: '#B4D79E' },
          { name: 'rubber', y: 0, color: '#AAFF00' },
          { name: 'other plantations', y: 0, color: '#F5F57A' },
          { name: 'rice', y: 0, color: '#FFFFBE' },
          { name: 'cropland', y: 0, color: '#FFD37F' },
          { name: 'surface water', y: 0, color: '#004DA8' },
          { name: 'grassland', y: 0, color: '#D7C29E' },
          { name: 'woodshrub', y: 0, color: '#89CD66' },
          { name: 'built-up area', y: 0, color: '#E600A9' },
          { name: 'village', y: 0, color: '#A900E6' },
          { name: 'other', y: 0, color: '#6f6f6f' }
        ];
        MapService.getLandcover(parameters)
          .then(function (data) {
            LandcoverData[area_id] = data;
            for (var i = studyLow; i <= studyHigh; i++) {

              var _yearData = data[i.toString()];
              var _year = i.toString();

              _yearArr.push(i);

              //total_burned_area = total_burned_area + _yearData.total_area;
              // 	for(var key in _yearData.total_area) {
              // 		for(var j=0; j<lcclass.length; j++){
              // 		if(lcclass[j].name === key){
              // 			lcclass[j].data.push(_yearData.total_area[key])
              // 		}
              // 	}
              // }
              if (map.hasLayer(MapLayerArr[_year].landcover)) {
                map.removeLayer(MapLayerArr[_year].landcover);
              }

              //add map layer
              MapLayerArr[_year].landcover = addMapLayer(MapLayerArr[_year].landcover, _yearData.eeMapURL, 'geeMapLayer');
              //set map style with opacity = 0.5
              MapLayerArr[_year].landcover.setOpacity(1);

              createToggleList('toggle-list-landcover', 'landcover' + _year, _year, _year, '', _yearData.color);
              //toggle each of forest map layer
              $("#landcover" + _year).change(function () {
                var layerID = $(this).attr('data-yid');
                if (this.checked) {
                  var toggleColor = $(this).attr('data-color');
                  $(this).closest("label").find("span").css("background-color", toggleColor);
                  MapLayerArr[layerID].landcover.addTo(map);

                } else {
                  $(this).closest("label").find("span").css("background-color", '#bbb');
                  if (map.hasLayer(MapLayerArr[layerID].landcover)) {
                    map.removeLayer(MapLayerArr[layerID].landcover);
                  }
                }
              });
            }

            $scope.showLoader = false;

          }, function (error) {
            console.log(error);
          });
      }
      getLandcover();
      // cal();


      function clearSelectAOI() {
        $("#nightlight-div").css("display", "none");
        _focusedAreas = [];
        timeSeriesArr = [];
        _barChartInfo = {
          "Education0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "edu_attain0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "edu_attend0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "Health0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "health_food0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "health_access0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "health_water0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "health_sanit0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "health_handwash0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "LivingStandard0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "liv_overcr0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "liv_hous0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "liv_cooking0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "liv_elect0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "liv_asset0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "liv_coping0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "Monetary0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
          "overall0": [
            { name: 'Not Deprived', data: [], color: '#434348' },
            { name: 'Deprived', data: [], color: '#7CB5EC' },
          ],
        };
      }

      /**
      * Change basemap layer(satellite, terrain, street)
      */
      $('input[type=radio][name=basemap_selection]').change(function () {
        var selected_basemap = $(this).val();

        // googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
        //     maxZoom: 20,
        //     subdomains:['mt0','mt1','mt2','mt3']
        // });
        // googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
        //     maxZoom: 20,
        //     subdomains:['mt0','mt1','mt2','mt3']
        // });
        // googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
        //     maxZoom: 20,
        //     subdomains:['mt0','mt1','mt2','mt3']
        // });
        // googleTerrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{
        //     maxZoom: 20,
        //     subdomains:['mt0','mt1','mt2','mt3']
        // });

        if (selected_basemap === "street") {
          basemap_layer.setUrl('https://api.mapbox.com/styles/v1/servirmekong/ckduef35613el19qlsoug6u2h/tiles/256/{z}/{x}/{y}@2x?access_token=' + MAPBOXAPI);
        } else if (selected_basemap === "satellite") {
          basemap_layer.setUrl('https://api.mapbox.com/styles/v1/servirmekong/ckecozln92fkk19mjhuoqxhuw/tiles/256/{z}/{x}/{y}@2x?access_token=' + MAPBOXAPI);
        } else if (selected_basemap === "terrain") {
          basemap_layer.setUrl('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}');
        }
      });

      $("#zoom-in").click(function () {
        map.zoomIn();
      });

      $("#zoom-out").click(function () {
        map.zoomOut();
      });

      $("#map-default").click(function () {
        map.setView([mapCenter_lat, mapCenter_long], 7);
      });

      $(".clear_map_button").click(function () {
        clearSelectAOI();
        selected_layers = [];
        cam_adm1_layer.eachLayer(function (layer) {
          cam_adm1_layer.resetStyle(layer);
        });
        cam_adm2_layer.eachLayer(function (layer) {
          cam_adm2_layer.resetStyle(layer);
        });
        cam_adm3_layer.eachLayer(function (layer) {
          cam_adm3_layer.resetStyle(layer);
        });


        $("#health0_chart_report_area").html("");
        $("#health_access0_chart_report_area").html("");
        $("#health_water0_chart_report_area").html("");
        $("#health_sanit0_chart_report_area").html("");
        $("#health_food0_chart_report_area").html("");
        $("#health_handwash0_chart_report_area").html("");
        $("#education0_chart_report_area").html("");
        $("#edu_attain0_chart_report_area").html("");
        $("#edu_attend0_chart_report_area").html("");

        $("#livingstandard0_chart_report_area").html("");
        $("#liv_overcr0_chart_report_area").html("");
        $("#liv_hous0_chart_report_area").html("");
        $("#liv_cooking0_chart_report_area").html("");
        $("#liv_asset0_chart_report_area").html("");
        $("#liv_coping0_chart_report_area").html("");
        $("#liv_elect0_chart_report_area").html("");

        $("#monetary0_chart_report_area").html("");
        $("#overall0_chart_report_area").html("");

      });


      $("#education0_bar_csv").click(function () {
        var chart = $("#education0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#education0_bar_png").click(function () {
        var chart = $("#education0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#edu_attain0_bar_csv").click(function () {
        var chart = $("#edu_attain0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#edu_attain0_bar_png").click(function () {
        var chart = $("#edu_attain0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#edu_attend0_bar_csv").click(function () {
        var chart = $("#edu_attend0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#edu_attend0_bar_png").click(function () {
        var chart = $("#edu_attend0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#health0_bar_csv").click(function () {
        var chart = $("#health0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#health0_bar_png").click(function () {
        var chart = $("#health0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#health_food0_bar_csv").click(function () {
        var chart = $("#health_food0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#health_food0_bar_png").click(function () {
        var chart = $("#health_food0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#health_access0_bar_csv").click(function () {
        var chart = $("#health_access0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#health_access0_bar_png").click(function () {
        var chart = $("#health_access0_barchart_adm").highcharts();
        chart.exportChart();
      });


      $("#health_water0_bar_csv").click(function () {
        var chart = $("#health_water0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#health_water0_bar_png").click(function () {
        var chart = $("#health_water0_barchart_adm").highcharts();
        chart.exportChart();
      });


      $("#health_sanit0_bar_csv").click(function () {
        var chart = $("#health_sanit0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#health_sanit0_bar_png").click(function () {
        var chart = $("#health_sanit0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#health_handwash0_bar_csv").click(function () {
        var chart = $("#health_handwash0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#health_handwash0_bar_png").click(function () {
        var chart = $("#health_handwash0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#livingstandard0_bar_csv").click(function () {
        var chart = $("#livingstandard0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#livingstandard0_bar_png").click(function () {
        var chart = $("#livingstandard0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#liv_overcr0_bar_csv").click(function () {
        var chart = $("#liv_overcr0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#liv_overcr0_bar_png").click(function () {
        var chart = $("#liv_overcr0_barchart_adm").highcharts();
        chart.exportChart();
      });


      $("#liv_hous0_bar_csv").click(function () {
        var chart = $("#liv_hous0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#liv_hous0_bar_png").click(function () {
        var chart = $("#liv_hous0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#liv_cooking0_bar_csv").click(function () {
        var chart = $("#liv_cooking0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#liv_cooking0_bar_png").click(function () {
        var chart = $("#liv_cooking0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#liv_elect0_bar_csv").click(function () {
        var chart = $("#liv_elect0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#liv_elect0_bar_png").click(function () {
        var chart = $("#liv_elect0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#liv_asset0_bar_csv").click(function () {
        var chart = $("#liv_asset0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#liv_asset0_bar_png").click(function () {
        var chart = $("#liv_asset0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#liv_coping0_bar_csv").click(function () {
        var chart = $("#liv_coping0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#liv_coping0_bar_png").click(function () {
        var chart = $("#liv_coping0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#monetary0_bar_csv").click(function () {
        var chart = $("#monetary0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#monetary0_bar_png").click(function () {
        var chart = $("#monetary0_barchart_adm").highcharts();
        chart.exportChart();
      });

      $("#overall0_bar_csv").click(function () {
        var chart = $("#overall0_barchart_adm").highcharts();
        chart.downloadCSV();
      });
      $("#overall0_bar_png").click(function () {
        var chart = $("#overall0_barchart_adm").highcharts();
        chart.exportChart();
      });


      function hideModel() {
        $(".modal").removeClass('show');
        $(".modal").addClass('hide');
      }

      $("#guiding-button").click(function () {
        hideModel();
        $("#guiding-modal").removeClass('hide');
        $("#guiding-modal").addClass('show');
      });
      $(".close").click(function () {
        $(".modal").removeClass('show');
        $(".modal").addClass('hide');
      });
      // Modal Close Function
      $(".modal-background").click(function () {
        $(".modal").removeClass('show');
        $(".modal").addClass('hide');
      });

      //////////////////////////////////////////////////

      /**
      * Toggle layer visualizing
      */
      $('input[type=checkbox][name=province_toggle]').click(function () {
        if (this.checked) {
          mapLayer_cam_adm1.addTo(map);
        } else {
          if (map.hasLayer(mapLayer_cam_adm1)) {
            map.removeLayer(mapLayer_cam_adm1);
          }
        }
      });
      $('input[type=checkbox][name=district_toggle]').click(function () {
        if (this.checked) {
          mapLayer_cam_adm2.addTo(map);
        } else {
          if (map.hasLayer(mapLayer_cam_adm2)) {
            map.removeLayer(mapLayer_cam_adm2);
          }
        }
      });

      $('input[type=checkbox][name=commune_toggle]').click(function () {
        if (this.checked) {
          mapLayer_cam_adm3.addTo(map);
        } else {
          if (map.hasLayer(mapLayer_cam_adm3)) {
            map.removeLayer(mapLayer_cam_adm3);
          }
        }
      });


      $('input[type=checkbox][name=dams_toggle]').click(function () {
        if (this.checked) {
          mapLayer_dams.addTo(map);
        } else {
          if (map.hasLayer(mapLayer_dams)) {
            map.removeLayer(mapLayer_dams);
          }
        }
      });

      $('input[type=checkbox][name=airport_toggle]').click(function () {
        if (this.checked) {
          mapLayer_airport.addTo(map);
        } else {
          if (map.hasLayer(mapLayer_airport)) {
            map.removeLayer(mapLayer_airport);
          }
        }
      });

      $('input[type=checkbox][name=main_road_toggle]').click(function () {
        if (this.checked) {
          mapLayer_main_road.addTo(map);
        } else {
          if (map.hasLayer(mapLayer_main_road)) {
            map.removeLayer(mapLayer_main_road);
          }
        }
      });

      $('input[type=checkbox][name=railway_toggle]').click(function () {
        if (this.checked) {
          mapLayer_railway.addTo(map);
        } else {
          if (map.hasLayer(mapLayer_railway)) {
            map.removeLayer(mapLayer_railway);
          }
        }
      });


      $("#administrative_level").change(function () {
        area_type = this.value;
        clearSelectAOI();
        $("#toggle-list-education").html('');
        $("#toggle-list-health").html('');
        $("#toggle-list-living").html('');
        $("#toggle-list-monetary").html('');
        $("#toggle-list-overall").html('');
        if (this.value === 'country') {
          $("#download_options").css("display", "none");
          cam_country_layer.addTo(map);
          if (map.hasLayer(cam_adm1_layer)) {
            map.removeLayer(cam_adm1_layer);
          }
          if (map.hasLayer(cam_adm2_layer)) {
            map.removeLayer(cam_adm2_layer);
          }
          if (map.hasLayer(cam_adm3_layer)) {
            map.removeLayer(cam_adm3_layer);
          }
        }
        else if (this.value === 'province') {
          $("#download_options").css("display", "none");
          createBarChart();
          cam_adm1_layer.addTo(map);
          if (map.hasLayer(cam_country_layer)) {
            map.removeLayer(cam_country_layer);
          }
          if (map.hasLayer(cam_adm2_layer)) {
            map.removeLayer(cam_adm2_layer);
          }
          if (map.hasLayer(cam_adm3_layer)) {
            map.removeLayer(cam_adm3_layer);
          }
        } else if (this.value === 'district') {
          $("#download_options").css("display", "none");
          createBarChart();
          cam_adm2_layer.addTo(map);
          if (map.hasLayer(cam_adm1_layer)) {
            map.removeLayer(cam_adm1_layer);
          }
          if (map.hasLayer(cam_country_layer)) {
            map.removeLayer(cam_country_layer);
          }
          if (map.hasLayer(cam_adm3_layer)) {
            map.removeLayer(cam_adm3_layer);
          }
        } else {
          $("#download_options").css("display", "block");
          cam_adm3_layer.addTo(map);
          if (map.hasLayer(cam_adm1_layer)) {
            map.removeLayer(cam_adm1_layer);
          }
          if (map.hasLayer(cam_country_layer)) {
            map.removeLayer(cam_country_layer);
          }
          if (map.hasLayer(cam_adm2_layer)) {
            map.removeLayer(cam_adm2_layer);
          }
        }
        getMapVal();
      })


      $(".close-menu").click(function () {
        $(".map-controller").css('left', '80px');
        $('.c-menu-panel').css('transform', ' translateX(-60rem)');
        $('.c-menu-panel').css('opacity', 0);
        $("#component1-tab").removeClass("active");
        $("#basemap-tab").removeClass("active");
        $("#component2-tab").removeClass("active");
        $("#component3-tab").removeClass("active");
        $("#layers-tab").removeClass("active");
        $("#usecase-tab").removeClass("active");
      });

      $("#component1-tab").click(function () {
        $(".close-menu").click();
        $(".map-controller").css('left', '420px');
        $("#component2-tab").removeClass("active");
        $("#component3-tab").removeClass("active");
        $("#layers-tab").removeClass("active");
        $(this).addClass("active");
        $('.c-menu-panel').css('transform', ' translateX(-60rem)');
        $('#panel-component1').css('transform', ' translateX(6.05rem)');
        $('#panel-component1').css('opacity', 1);
      });

      $("#component2-tab").click(function () {
        $(".close-menu").click();
        $(".map-controller").css('left', '420px');
        $("#component1-tab").removeClass("active");
        $("#component3-tab").removeClass("active");
        $("#layers-tab").removeClass("active");
        $(this).addClass("active");
        $('.c-menu-panel').css('transform', ' translateX(-60rem)');
        $('#panel-component2').css('transform', ' translateX(6.05rem)');
        $('#panel-component2').css('opacity', 1);
      });

      $("#component3-tab").click(function () {
        $(".close-menu").click();
        $(".map-controller").css('left', '420px');
        $("#component1-tab").removeClass("active");
        $("#component2-tab").removeClass("active");
        $("#layers-tab").removeClass("active");
        $(this).addClass("active");
        $('.c-menu-panel').css('transform', ' translateX(-60rem)');
        $('#panel-component3').css('transform', ' translateX(6.05rem)');
        $('#panel-component3').css('opacity', 1);
      });

      $("#layers-tab").click(function () {
        $(".close-menu").click();
        $(".map-controller").css('left', '420px');
        $("#component2-tab").removeClass("active");
        $("#component1-tab").removeClass("active");
        $("#component3-tab").removeClass("active");
        $(this).addClass("active");
        $('.c-menu-panel').css('transform', ' translateX(-60rem)');
        $('#panel-layers').css('transform', ' translateX(6.05rem)');
        $('#panel-layers').css('opacity', 1);
      });


      $("#clipboardFunc").click(function () {
        var copyText = document.getElementById("downloadURL_box");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        navigator.clipboard.writeText(copyText.value);
        var tooltip = document.getElementById("downloadURL_box");
        tooltip.innerHTML = "Copied: " + copyText.value;
      });

      $("#download_commu_csv").click(function () {
        var parameters = { type: 'csv' };
        MapService.getDownloadURL(parameters)
          .then(function (data) {
            // $scope.showLoader = true;
            $("#downloadURL_box").val(data.downloadUrl);
            //showInfoAlert("Please wait for few minutes we are processing your request!");
            // download(data.downloadUrl, "cambodia_poverty_valnerability_adm3_csv");
          }, function (error) {
            console.log(error);
          });
      });


      $("#download_commu_shp").click(function () {
        var parameters = { type: 'shp' };
        MapService.getDownloadURL(parameters)
          .then(function (data) {
            // $scope.showLoader = true;
            $("#downloadURL_box").val(data.downloadUrl);
            //showInfoAlert("Please wait for few minutes we are processing your request!");
            // download(data.downloadUrl, "cambodia_poverty_valnerability_adm3_shp")
          }, function (error) {
            console.log(error);
          });
      });
    });

})();
