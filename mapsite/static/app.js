var berlin = {lat: 52.52, lng: 13.405};
var map_options = {
  zoom: 12,
  center: berlin,
  scrollwheel: false,
}

var map, marker, geocoder;

/** Initialize google maps, geocoder and register click event */
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), map_options);
  geocoder = new google.maps.Geocoder();
  map.addListener('click', function(e) {
    getGeocodeInfo(e, map);
  });
}

/**
 * Place a marker on the map and pan the view to this marker.
 * @param {Object} position - The lat / long coordinates object.
 * @param {Object} map - The google map object.
 */
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

/**
 * Call the geocoder to retrieve geo info of the clicked position.
 * @param {Object} e - The click event.
 * @param {Object} map - The google map object.
 */
function getGeocodeInfo(e, map) {
  geocoder.geocode({
    'latLng': e.latLng
  }, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results[0] && results[0].types[0] == CONFIG.mapsType) {
        var addressesDiv = document.getElementById("addresses");
        addressesDiv.innerHTML = "<p>Updating...</p>";
        placeMarker(e.latLng, map);
        postAddress({
            lat:e.latLng.lat().toFixed(6), lon:e.latLng.lng().toFixed(6),
            full_address:results[0].formatted_address
        });
      }
    }
  });
}

/**
 * AJAX post the address object to the backend.
 * @param {Object} address - The address object.
 */
function postAddress(address) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', CONFIG.postUrl);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (xhr.status === 200) {
      renderAddresses(JSON.parse(xhr.responseText));
    }
    else if (xhr.status !== 200) {
      console.log(xhr.responseText);
      var addressesDiv = document.getElementById("addresses");
      addressesDiv.innerHTML = "<p>Updating Failed.</p>";
    }
  };
  xhr.send(encodeObject(address));
}

/**
 * Encode json object for AJAX call.
 * @param {Object} object - The object to encode.
 * @returns {string}
 */
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

/**
 * Render new addresses over old addresses.
 * @param {Object[]} addresses - The list of addresses to render.
 */
function renderAddresses(addresses) {
  var addressesDiv = document.getElementById("addresses");
  var addressesHtml = "";
  addresses.forEach(function(address) {
    addressesHtml += "<p>" + address.full_address + "</p>";
  });
  addressesDiv.innerHTML = addressesHtml;
}
