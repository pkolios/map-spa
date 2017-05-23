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
        postAddress({
            lat:e.latLng.lat().toFixed(6), lon:e.latLng.lng().toFixed(6),
            full_address:results[0].formatted_address
        });
      }
    }
  });
}

function postAddress(address) {
  // lat, lon, full_address
  var xhr = new XMLHttpRequest();
  xhr.open('POST', CONFIG.postUrl);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (xhr.status === 200) {
      renderAddresses(JSON.parse(xhr.responseText));
    }
    else if (xhr.status !== 200) {
      console.log(xhr.responseText);
    }
  };
  xhr.send(encodeObject(address));
}

function encodeObject(object) {
  var encodedString = '';
  for (var prop in object) {
    if (object.hasOwnProperty(prop)) {
      if (encodedString.length > 0) {
        encodedString += '&';
      }
      encodedString += encodeURI(prop + '=' + object[prop]);
    }
  }
  return encodedString;
}

function renderAddresses(addresses) {
  var addressesDiv = document.getElementById("addresses");
  var addressesHtml = "";
  addresses.forEach(function(address) {
    addressesHtml += "<p>" + address.full_address + "</p>";
  });
  addressesDiv.innerHTML = addressesHtml;
}
