window.marker = null;

function initialize() {
  var map;
  var latitude = $('#map').attr('data-latitude');
  var longitude = $('#map').attr('data-longitude');
  var map_marker = $('#map').attr('data-marker');
  var nottingham = new google.maps.LatLng(latitude, longitude);
  var style = [{
      "featureType": "all",
      "elementType": "labels.text.fill",
      "stylers": [{
          "saturation": 36
        },
        {
          "color": "#333333"
        },
        {
          "lightness": 40
        }
      ]
    },
    {
      "featureType": "all",
      "elementType": "labels.text.stroke",
      "stylers": [{
          "visibility": "on"
        },
        {
          "color": "#ffffff"
        },
        {
          "lightness": 16
        }
      ]
    },
    {
      "featureType": "all",
      "elementType": "labels.icon",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "administrative",
      "elementType": "geometry.fill",
      "stylers": [{
          "color": "#fefefe"
        },
        {
          "lightness": 20
        }
      ]
    },
    {
      "featureType": "administrative",
      "elementType": "geometry.stroke",
      "stylers": [{
          "color": "#fefefe"
        },
        {
          "lightness": 17
        },
        {
          "weight": 1.2
        }
      ]
    },
    {
      "featureType": "administrative.province",
      "elementType": "labels.text",
      "stylers": [{
          "saturation": "22"
        },
        {
          "color": "#ff0000"
        },
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "administrative.province",
      "elementType": "labels.text.fill",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "administrative.locality",
      "elementType": "labels.text.fill",
      "stylers": [{
          "color": "#d84508"
        },
        {
          "saturation": "51"
        },
        {
          "lightness": "6"
        }
      ]
    },
    {
      "featureType": "administrative.neighborhood",
      "elementType": "labels.text.fill",
      "stylers": [{
          "color": "#0a0101"
        },
        {
          "lightness": "-61"
        },
        {
          "saturation": "-24"
        },
        {
          "gamma": "0.72"
        }
      ]
    },
    {
      "featureType": "administrative.land_parcel",
      "elementType": "labels.text.fill",
      "stylers": [{
        "color": "#000000"
      }]
    },
    {
      "featureType": "landscape",
      "elementType": "geometry",
      "stylers": [{
          "color": "#f5f5f5"
        },
        {
          "lightness": 20
        }
      ]
    },
    {
      "featureType": "poi",
      "elementType": "geometry",
      "stylers": [{
          "color": "#f5f5f5"
        },
        {
          "lightness": 21
        }
      ]
    },
    {
      "featureType": "poi.business",
      "elementType": "all",
      "stylers": [{
        "visibility": "on"
      }]
    },
    {
      "featureType": "poi.business",
      "elementType": "labels.icon",
      "stylers": [{
          "color": "#e34c0e"
        },
        {
          "saturation": "21"
        },
        {
          "lightness": "13"
        }
      ]
    },
    {
      "featureType": "poi.government",
      "elementType": "all",
      "stylers": [{
        "visibility": "on"
      }]
    },
    {
      "featureType": "poi.government",
      "elementType": "labels.icon",
      "stylers": [{
          "color": "#000000"
        },
        {
          "weight": "1.00"
        }
      ]
    },
    {
      "featureType": "poi.park",
      "elementType": "all",
      "stylers": [{
        "visibility": "on"
      }]
    },
    {
      "featureType": "poi.park",
      "elementType": "geometry",
      "stylers": [{
          "color": "#dedede"
        },
        {
          "lightness": 21
        }
      ]
    },
    {
      "featureType": "poi.park",
      "elementType": "geometry.fill",
      "stylers": [{
        "color": "#dfdfdf"
      }]
    },
    {
      "featureType": "poi.park",
      "elementType": "labels.text",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "poi.park",
      "elementType": "labels.text.fill",
      "stylers": [{
          "color": "#d84508"
        },
        {
          "saturation": "31"
        }
      ]
    },
    {
      "featureType": "road.highway",
      "elementType": "geometry.fill",
      "stylers": [{
          "color": "#ffffff"
        },
        {
          "lightness": 17
        }
      ]
    },
    {
      "featureType": "road.highway",
      "elementType": "geometry.stroke",
      "stylers": [{
          "color": "#ffffff"
        },
        {
          "lightness": 29
        },
        {
          "weight": 0.2
        }
      ]
    },
    {
      "featureType": "road.arterial",
      "elementType": "geometry",
      "stylers": [{
          "color": "#ffffff"
        },
        {
          "lightness": 18
        }
      ]
    },
    {
      "featureType": "road.arterial",
      "elementType": "labels.text.fill",
      "stylers": [{
        "color": "#3a3a3a"
      }]
    },
    {
      "featureType": "road.local",
      "elementType": "geometry",
      "stylers": [{
          "color": "#ffffff"
        },
        {
          "lightness": 16
        }
      ]
    },
    {
      "featureType": "road.local",
      "elementType": "labels.text.fill",
      "stylers": [{
          "color": "#000000"
        },
        {
          "lightness": "42"
        },
        {
          "saturation": "7"
        },
        {
          "visibility": "off"
        }
      ]
    },
    {
      "featureType": "transit",
      "elementType": "geometry",
      "stylers": [{
          "color": "#f2f2f2"
        },
        {
          "lightness": 19
        }
      ]
    },
    {
      "featureType": "water",
      "elementType": "geometry",
      "stylers": [{
          "color": "#e9e9e9"
        },
        {
          "lightness": 17
        }
      ]
    }
  ];
  var mapOptions = {
    center: nottingham,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    backgroundColor: "#000",
    zoom: 15,
    panControl: false,
    zoomControl: true,
    mapTypeControl: false,
    scaleControl: false,
    streetViewControl: false,
    overviewMapControl: false,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.LARGE
    }
  }
  map = new google.maps.Map(document.getElementById('map'), mapOptions);
  var mapType = new google.maps.StyledMapType(style, {
    name: "Grayscale"
  });
  map.mapTypes.set('grey', mapType);
  map.setMapTypeId('grey');
  var marker_image = map_marker;
  var pinIcon = new google.maps.MarkerImage(marker_image, null, null, null, new google.maps.Size(46, 50));
  marker = new google.maps.Marker({
    position: nottingham,
    map: map,
    icon: pinIcon,
    title: 'Orbitor'
  });
}
var map = document.getElementById('map');
if (map != null) {
  google.maps.event.addDomListener(window, 'load', initialize);
}