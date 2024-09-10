(function () {

	'use strict';

	angular.module('baseApp')
	.service('MapService', function ($http, $q) {
		var service = this;

		service.getMapType = function (mapId, mapToken, type) {
			var eeMapOptions = {
				getTileUrl: function (tile, zoom) {
					var url = 'https://earthengine.googleapis.com/map/';
					url += [mapId, zoom, tile.x, tile.y].join('/');
					url += '?token=' + mapToken;
					return url;
				},
				tileSize: new google.maps.Size(256, 256),
				opacity: 1.0,
				name: type
			};
			return new google.maps.ImageMapType(eeMapOptions);
		};


		service.checkAvailableData= function (options) {
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					polygon_id:options.polygon_id,
					startYear: options.startYear,
					endYear:options.endYear,
					area_type: options.area_type,
					area_id: options.area_id,
				},
				params: {
					action: 'check-date'
				}
			};

			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};

		service.getMapVal= function (options) {
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					feat:options.feat,
					area_type: options.area_type,
					area_id: options.area_id,
				},
				params: {
					action: 'get-val-map'
				}
			};
			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};

		service.getDownloadURL= function (options) {
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {type:options.type,},
				params: {
					action: 'get-download-url'
				}
			};
			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};



		service.getNightTimeSeriesVal= function (options) {
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					area_type: options.area_type,
					lon:options.lon,
					lat: options.lat,
				},
				params: {
					action: 'get-nightlight-series'
				}
			};
			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};


		service.getGraphPieData= function (options) {
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					feat:options.feat,
					area_type: options.area_type,
					area_id: options.area_id,
				},
				params: {
					action: 'get-graph-pie-data'
				}
			};
			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};

		service.getPropMap= function (options) {
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					area_type: options.area_type,
					area_id: options.area_id,
				},
				params: {
					action: 'get-prop-map'
				}
			};
			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};

		service.getNightLightMap= function (options) {
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					startYear: options.startYear,
					endYear:options.endYear,
					area_type: options.area_type,
					area_id: options.area_id,
				},
				params: {
					action: 'get-nightlight'
				}
			};
			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};



		service.getMapData= function (options) {
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					polygon_id:options.polygon_id,
					startYear: options.startYear,
					endYear:options.endYear,
					area_type: options.area_type,
					area_id: options.area_id,
					data: options.data,
				},
				params: {
					action: 'calMapArea'
				}
			};
			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};


		service.getGraphData= function (options) {
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					polygon_id:options.polygon_id,
					startYear: options.startYear,
					endYear:options.endYear,
					area_type: options.area_type,
					area_id: options.area_id,
					data: options.data,
				},
				params: {
					action: 'get-graph-data'
				}
			};
			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};


		service.getOthersMap= function (options) {
			var area_type = options.area_type;
			var area_id = options.area_id;
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					area_type: options.area_type,
					area_id: options.area_id,
				},
				params: {
					action: 'get-building-map'
				}
			};
			var promise = $http(req)
			.then(function (response) {
				return response.data;
			});
			return promise;
		};

		service.getForestMapID = function (options) {
			var startYear = options.startYear;
			var endYear = options.endYear;
			var polygon_id = options.polygon_id;
			var treeCanopyDefinition = options.treeCanopyDefinition;
			var treeHeightDefinition = options.treeHeightDefinition;
			var type = options.type; // can be treeCanopy, forestGain, forestLoss or forestExtend\
			var download = options.download;
			var year = options.year;
			var action = ''
			if(download === false){
				action = 'get-forest-extent-map';
			}else{
				action = 'download-forest-extent-map';
			}

			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					polygon_id: polygon_id,
					type: type,
					startYear: startYear,
					endYear: endYear,
					treeCanopyDefinition: treeCanopyDefinition,
					treeHeightDefinition: treeHeightDefinition,
					area_type: options.area_type,
					area_id: options.area_id,
					year: year
				},
				params: {
					action: action,
					type: type
				}
			};

			var promise = $http(req)
			.then(function (response) {
				return response.data;
			})
			.catch(function (e) {
				console.log('Error: ', e);
				throw e.data;
			});
			return promise;
		};


		service.getLandcover= function (options) {
			var startYear = options.startYear;
			var endYear = options.endYear;
			var polygon_id = options.polygon_id;
			var area_type = options.area_type;
			var area_id = options.area_id;
			var year = options.year;
			var download = options.download;
			var action = ''
			if(download === true){
				action= 'download-landcover'
			}else{
				action= 'get-landcover'
			}
			var req = {
				method: 'POST',
				url: '/api/mapclient/',
				data: {
					polygon_id: polygon_id,
					startYear: startYear,
					endYear: endYear,
					area_type: area_type,
					area_id: area_id,
					year: year,
					download: download
				},
				params: {
					action: action
				}
			};

			var promise = $http(req)
			.then(function (response) {
				return response.data;
			})
			.catch(function (e) {
				console.log('Error: ', e);
				throw e.data;
			});
			return promise;
		};

		service.removeGeoJson = function (map) {
			map.data.forEach(function (feature) {
				map.data.remove(feature);
			});
		};

		service.clearLayer = function (map, name) {
			map.overlayMapTypes.forEach(function (layer, index) {
				if (layer && layer.name === name) {
					map.overlayMapTypes.removeAt(index);
				}
			});
		};

		// Remove the Drawing Manager Polygon
		service.clearDrawing = function (overlay) {
			if (overlay) {
				overlay.setMap(null);
			}
		};

		service.getPolygonBoundArray = function (array) {
			var geom = [];
			for (var i = 0; i < array.length; i++) {
				var coordinatePair = [array[i].lng().toFixed(2), array[i].lat().toFixed(2)];
				geom.push(coordinatePair);
			}
			return geom;
		};


	});

})();
