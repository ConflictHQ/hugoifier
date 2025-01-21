window.marker = null;

function initialize() {
  var map;
  var latitude = $('#map_canvas').attr('data-latitude');
  var longitude = $('#map_canvas').attr('data-longitude');
  var mapMarker = $('#map_canvas').attr('data-marker');
  var mapMarkerName = $('#map_canvas').attr('data-marker-name');
  var nottingham = new google.maps.LatLng(latitude, longitude);
  var style = [{
      "featureType": "all",
      "elementType": "labels.text.fill",
      "stylers": [{
        "color": "#a8afbf"
      }]
    },
    {
      "featureType": "all",
      "elementType": "labels.text.stroke",
      "stylers": [{
          "visibility": "on"
        },
        {
          "color": "#373d48"
        },
        {
          "weight": 2
        },
        {
          "gamma": "1"
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
      "elementType": "geometry",
      "stylers": [{
          "weight": 0.6
        },
        {
          "color": "#4c576f"
        },
        {
          "gamma": "0"
        }
      ]
    },
    {
      "featureType": "landscape",
      "elementType": "geometry",
      "stylers": [{
          "color": "#424c65"
        },
        {
          "gamma": "1"
        },
        {
          "weight": "10"
        }
      ]
    },
    {
      "featureType": "poi",
      "elementType": "geometry",
      "stylers": [{
        "color": "#4c576f"
      }]
    },
    {
      "featureType": "poi.park",
      "elementType": "geometry",
      "stylers": [{
        "color": "#424d66"
      }]
    },
    {
      "featureType": "road",
      "elementType": "geometry",
      "stylers": [{
          "color": "#37425c"
        },
        {
          "lightness": "0"
        }
      ]
    },
    {
      "featureType": "transit",
      "elementType": "geometry",
      "stylers": [{
        "color": "#4c576f"
      }]
    },
    {
      "featureType": "water",
      "elementType": "geometry",
      "stylers": [{
        "color": "#2b364f"
      }]
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
  map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
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
    title: mapMarkerName
  });
}
var map = document.getElementById('map_canvas');
if (map != null) {
  google.maps.event.addDomListener(window, 'load', initialize);
}