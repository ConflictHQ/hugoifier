window.marker = null;

function initialize() {
  var map;
  var latitude = $('#map').attr('data-latitude');
  var longitude = $('#map').attr('data-longitude');
  var mapMarker = $('#map').attr('data-marker');
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
      "elementType": "all",
      "stylers": [{
        "visibility": "on"
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
      "featureType": "administrative.country",
      "elementType": "labels",
      "stylers": [{
        "visibility": "on"
      }]
    },
    {
      "featureType": "administrative.province",
      "elementType": "labels",
      "stylers": [{
          "visibility": "on"
        },
        {
          "hue": "#ff0000"
        }
      ]
    },
    {
      "featureType": "administrative.province",
      "elementType": "labels.text",
      "stylers": [{
          "color": "#727272"
        },
        {
          "weight": "0.30"
        }
      ]
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
      "featureType": "landscape.man_made",
      "elementType": "all",
      "stylers": [{
        "visibility": "on"
      }]
    },
    {
      "featureType": "landscape.natural.landcover",
      "elementType": "all",
      "stylers": [{
        "visibility": "on"
      }]
    },
    {
      "featureType": "landscape.natural.landcover",
      "elementType": "geometry.fill",
      "stylers": [{
          "visibility": "off"
        },
        {
          "color": "#ffb500"
        }
      ]
    },
    {
      "featureType": "poi",
      "elementType": "all",
      "stylers": [{
        "visibility": "off"
      }]
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
      "featureType": "road",
      "elementType": "geometry.fill",
      "stylers": [{
          "visibility": "on"
        },
        {
          "color": "#ffb500"
        }
      ]
    },
    {
      "featureType": "road",
      "elementType": "labels.text.fill",
      "stylers": [{
        "color": "#ffb500"
      }]
    },
    {
      "featureType": "road.highway",
      "elementType": "geometry.fill",
      "stylers": [{
          "color": "#ffb500"
        },
        {
          "lightness": 17
        },
        {
          "visibility": "on"
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
      "featureType": "transit",
      "elementType": "all",
      "stylers": [{
        "visibility": "on"
      }]
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
      "featureType": "transit",
      "elementType": "geometry.fill",
      "stylers": [{
        "color": "#ffb500"
      }]
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
    },
    {
      "featureType": "water",
      "elementType": "geometry.fill",
      "stylers": [{
          "visibility": "on"
        },
        {
          "color": "#ffb500"
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
  var marker_image = mapMarker;
  var pinIcon = new google.maps.MarkerImage(marker_image, null, null, null, new google.maps.Size(46, 50));
  marker = new google.maps.Marker({
    position: nottingham,
    map: map,
    icon: pinIcon,
    title: 'WishFund'
  });
}
var map = document.getElementById('map');
if (map != null) {
  google.maps.event.addDomListener(window, 'load', initialize);
}