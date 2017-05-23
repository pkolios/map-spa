var berlin = {lat: 52.52, lng: 13.405};
var map_options = {
  zoom: 12,
  center: berlin,
  scrollwheel: false,
}

var map, marker, geocoder;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), map_options);
  geocoder = new google.maps.Geocoder();
  map.addListener('click', function(e) {
    handleClick(e, map);
  });
}

function handleClick(e, map) {
  getGeocodeInfo(e);
  placeMarker(e.latLng, map);
}

function placeMarker(position, map) {
  if (marker !== undefined) {
    marker.setMap(null);
  }
  marker = new google.maps.Marker({
    position: position,
    map: map
  });
  map.panTo(position);
}

function getGeocodeInfo(e) {
  geocoder.geocode({
    'latLng': e.latLng
  }, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        // Validate real address & ajax call to backend here
        console.log(results);
      }
    }
  });
}
