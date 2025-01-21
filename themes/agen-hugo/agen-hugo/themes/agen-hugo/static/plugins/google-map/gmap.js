window.marker = null;

function initialize() {
  var map;
  var latitude = $('#map_canvas').attr('data-latitude');
  var longitude = $('#map_canvas').attr('data-longitude');
  var mapMarker = $('#map_canvas').attr('data-marker');
  var nottingham = new google.maps.LatLng(latitude, longitude);
  var style = [{
      "featureType": "administrative",
      "elementType": "labels.text",
      "stylers": [{
        "visibility": "on"
      }]
    },
    {
      "featureType": "poi",
      "elementType": "all",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "transit.station.rail",
      "elementType": "all",
      "stylers": [{
          "visibility": "simplified"
        },
        {
          "saturation": "-100"
        }
      ]
    },
    {
      "featureType": "water",
      "elementType": "all",
      "stylers": [{
        "visibility": "on"
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
  var pinIcon = new google.maps.MarkerImage(marker_image, null, null, null, new google.maps.Size(60, 88));
  marker = new google.maps.Marker({
    position: nottingham,
    map: map,
    icon: pinIcon,
    title: 'Agen'
  });
}
var map = document.getElementById('map_canvas');
if (map != null) {
  google.maps.event.addDomListener(window, 'load', initialize);
}