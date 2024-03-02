/*
This script expects:

<input type="text" name="address" id="id_locations-{index}-address" />
<input type="text" name="geolocation" id="id_locations-{index}-geolocation" />
*/

class LocationFormGoogleMap {
  constructor(index) {
    this.index = index;
    this.autocomplete = null;
    this.geocoder = new google.maps.Geocoder();
    this.map = null;
    this.marker = null;
    this.geolocationId = `id_locations-${index}-geolocation`;
    this.addressId = `id_locations-${index}-address`;
    this.mapCanvasId = `locations-${index}-address_map_canvas`;
  }

  initialize() {
    let lat = 0;
    let lng = 0;
    let zoom = 2;

    // Update zoom level and initial cordinates if form is bound
    const existingLocation = this.getExistingLocation();
    if (existingLocation) {
      lat = existingLocation[0];
      lng = existingLocation[1];
      zoom = 12;
    }

    const latlng = new google.maps.LatLng(lat, lng);
    const mapOptions = {
      zoom: zoom,
      center: latlng,
      mapTypeId: this.getMapType(),
    };
    this.map = new google.maps.Map(document.getElementById(this.mapCanvasId), mapOptions);

    if (existingLocation) this.setMarker(latlng);

    this.autocomplete = new google.maps.places.Autocomplete(
      document.getElementById(this.addressId),
      this.getAutoCompleteOptions()
    );

    this.autocomplete.addListener("place_changed", () => this.codeAddress());

    $(`#${this.addressId}`).keydown(function (e) {
      if (e.keyCode == 13) {
        e.preventDefault();
        return false;
      }
    });
  }

  getMapType() {
    const geolocationInput = document.getElementById(this.addressId);
    const allowedType = ["roadmap", "satellite", "hybrid", "terrain"];
    const mapType = geolocationInput.getAttribute("data-map-type");

    if (mapType && -1 !== allowedType.indexOf(mapType)) return mapType;
    return google.maps.MapTypeId.HYBRID;
  }

  getAutoCompleteOptions() {
    const geolocationInput = document.getElementById(this.addressId);
    const autocompleteOptions = geolocationInput.getAttribute(
      "data-autocomplete-options"
    );

    if (!autocompleteOptions) return { types: ["geocode"] };
    return JSON.parse(autocompleteOptions);
  }

  getExistingLocation() {
    const geolocationInput = document.getElementById(this.geolocationId);
    if (geolocationInput && geolocationInput.value) {
      return geolocationInput.value.split(",");
    }
  }

  codeAddress() {
    const place = this.autocomplete.getPlace();

    if (place.geometry !== undefined) {
      this.updateWithCoordinates(place.geometry.location);
    } else {
      this.geocoder.geocode({ address: place.name }, (results, status) => {
        if (status == google.maps.GeocoderStatus.OK) {
          const latlng = results[0].geometry.location;
          this.updateWithCoordinates(latlng);
        } else {
          alert("Geocode was not successful for the following reason: " + status);
        }
      });
    }
  }

  updateWithCoordinates(latlng) {
    this.map.setCenter(latlng);
    this.map.setZoom(18);
    this.setMarker(latlng);
    this.updateGeolocation(latlng);
  }

  setMarker(latlng) {
    this.marker
      ? this.updateMarker(latlng)
      : this.addMarker({ latlng: latlng, draggable: true });
  }

  addMarker(Options) {
    this.marker = new google.maps.Marker({
      map: this.map,
      position: Options.latlng,
    });

    const draggable = Options.draggable || false;
    if (draggable) {
      this.addMarkerDrag(this.marker);
    }
  }

  addMarkerDrag(marker) {
    marker.setDraggable(true);
    google.maps.event.addListener(marker, "dragend", (new_location) => {
      this.updateGeolocation(new_location.latLng);
    });
  }

  updateMarker(latlng) {
    this.marker.setPosition(latlng);
  }

  updateGeolocation(latlng) {
    document.getElementById(this.geolocationId).value = latlng.lat() + "," + latlng.lng();
    $(`#${this.geolocationId}`).trigger("change");
  }
}

$(document).ready(function () {
  const addressInputSelector = "input[id^='id_locations-'][id$='-address']:visible";

  // Initialize existing location forms
  $(addressInputSelector).each(function (index) {
    new LocationFormGoogleMap(index).initialize();
  });

  // Listen and check for insertion of new location forms
  $(document).bind("formset:added", function (e) {
    const newAddressInput = $(e.target).find(addressInputSelector);

    if (newAddressInput) {
      const index = parseInt(newAddressInput.attr("id").match(/(?<=-)\d+(?=-)/)[0]);
      new LocationFormGoogleMap(index).initialize();
    }
  });
});
