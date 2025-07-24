/*
Integration for Google Maps in the django admin.

How it works:

You have an address field on the page.
Enter an address and an on change event will update the map
with the address. A marker will be placed at the address.
If the user needs to move the marker, they can and the geolocation
field will be updated.

Only one marker will remain present on the map at a time.

This script expects:

<input type="text" name="address" id="id_address" />
<input type="text" name="geolocation" id="id_geolocation" />

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

*/

function googleMapAdmin() {

    var autocomplete;
    var geocoder;
    var map;
    var marker;

    var geolocationId = 'id_geolocation';
    var addressId = 'id_address';
    var messageBoxId = 'map_message_box';

    var self = {
        /**
         * Initializes the Google Map, Autocomplete, and sets up event listeners.
         */
        initialize: function () {
            // Initialize Geocoder
            geocoder = new google.maps.Geocoder();
            var lat = 0;
            var lng = 0;
            var zoom = 2; // Default to world view

            // Get existing location from the geolocation input field
            var existingLocation = self.getExistingLocation();

            if (existingLocation) {
                lat = parseFloat(existingLocation[0]); // Ensure latitude is a number
                lng = parseFloat(existingLocation[1]); // Ensure longitude is a number
                zoom = 18; // Zoom in if a location already exists
            }

            // Create a LatLng object for the map center
            var latlng = {lat: lat, lng: lng};
            var myOptions = {
                zoom: zoom,
                center: latlng,
                mapTypeId: self.getMapType(),
                streetViewControl: false,
                mapTypeControl: true,
                fullscreenControl: false
            };

            // Create the map instance
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

            // If an existing location is present, set a marker
            if (existingLocation) {
                self.setMarker(latlng);
            }

            // Initialize Google Places Autocomplete on the address input field
            autocomplete = new google.maps.places.Autocomplete(
                /** @type {!HTMLInputElement} */(document.getElementById(addressId)),
                self.getAutoCompleteOptions());

            // Add listener for when a place is selected from the autocomplete suggestions
            // This triggers when the user presses enter or selects a suggestion
            autocomplete.addListener("place_changed", self.codeAddress);

            // Prevent the 'Enter' key from submitting the form when in the address field.
            // Instead, it should trigger the place_changed event for autocomplete.
            document.getElementById(addressId).addEventListener("keydown", function (e) {
                if (e.key === "Enter") {
                    e.preventDefault();
                    return false;
                }
            });
        },

        /**
         * Determines the map type based on a 'data-map-type' attribute on the address input.
         * Falls back to 'hybrid' if not specified or invalid.
         * @returns {string} The map type string (e.g., 'roadmap', 'satellite').
         */
        getMapType: function () {
            // https://developers.google.com/maps/documentation/javascript/maptypes
            var addressInput = document.getElementById(addressId);
            var allowedTypes = ['roadmap', 'satellite', 'hybrid', 'terrain'];
            var mapType = addressInput.getAttribute('data-map-type');

            if (mapType && allowedTypes.includes(mapType)) {
                return mapType;
            }

            return 'hybrid'; // Default to hybrid map type
        },

        /**
         * Retrieves autocomplete options from a 'data-autocomplete-options' attribute.
         * Defaults to geocode type if not specified.
         * @returns {object} Autocomplete options object.
         */
        getAutoCompleteOptions: function () {
            var addressInput = document.getElementById(addressId);
            var autocompleteOptions = addressInput.getAttribute('data-autocomplete-options');

            if (!autocompleteOptions) {
                return {
                    types: ['geocode']
                };
            }

            try {
                return JSON.parse(autocompleteOptions);
            } catch (e) {
                console.error("Error parsing data-autocomplete-options:", e);
                self.showMessage("Error: Invalid autocomplete options format. Using default.", 'error');
                return {types: ['geocode']};
            }
        },

        /**
         * Retrieves existing latitude and longitude from the geolocation input field.
         * @returns {Array<string>|undefined} An array [latitude, longitude] or undefined if empty.
         */
        getExistingLocation: function () {
            var geolocationInput = document.getElementById(geolocationId).value;
            if (geolocationInput) {
                return geolocationInput.split(',');
            }
            return undefined;
        },

        /**
         * Geocodes the address entered in the autocomplete field.
         * Updates the map and marker based on the geocoded location.
         */
        codeAddress: function () {
            var place = autocomplete.getPlace();

            // Checkifa place with geometry (location) was found by Autocomplete
            if (place.geometry && place.geometry.location) {
                self.updateWithCoordinates(place.geometry.location);
            } else if (place.name) {
                // If no geometry, but a place name exists, try to geocode it
                geocoder.geocode({'address': place.name}, function (results, status) {
                    if (status === 'OK' && results.length > 0) {
                        var latlng = results[0].geometry.location;
                        self.updateWithCoordinates(latlng);
                    } else if (status === 'ZERO_RESULTS') {
                        self.showMessage("No results found for '" + place.name + "'.", 'warning');
                    } else {
                        self.showMessage("Geocode was not successful for the following reason: " + status, 'error');
                    }
                });
            } else {
                self.showMessage("Please enter a valid address.", 'warning');
            }
        },

        /**
         * Updates the map center, zoom, marker, and geolocation input with new coordinates.
         * @param {google.maps.LatLng} latlng - The new LatLng object.
         */
        updateWithCoordinates: function (latlng) {
            map.setCenter(latlng);
            map.setZoom(18);
            self.setMarker(latlng);
            self.updateGeolocation(latlng);
        },

        /**
         * Sets or updates the map marker at the given LatLng.
         * @param {google.maps.LatLng} latlng - The LatLng for the marker.
         */
        setMarker: function (latlng) {
            if (marker) {
                self.updateMarker(latlng);
            } else {
                self.addMarker({'latlng': latlng, 'draggable': true});
            }
        },

        /**
         * Adds a new marker to the map.
         * @param {object} Options - Marker options, including latlng and draggable.
         */
        addMarker: function (Options) {
            marker = new google.maps.Marker({
                map: map,
                position: Options.latlng
            });

            var draggable = Options.draggable || false;
            if (draggable) {
                self.addMarkerDrag();
            }
        },

        /**
         * Adds a 'dragend' listener to the marker to update geolocation when dragged.
         */
        addMarkerDrag: function () {
            marker.setDraggable(true);
            // Use the modern addListener method
            marker.addListener('dragend', function (event) {
                self.updateGeolocation(event.latLng);
            });
        },

        /**
         * Updates the position of the existing marker.
         * @param {google.maps.LatLng} latlng - The new LatLng for the marker.
         */
        updateMarker: function (latlng) {
            marker.setPosition(latlng);
        },

        /**
         * Updates the geolocation input field with the new latitude and longitude.
         * Manually dispatches a 'change' event for compatibility with other scripts.
         * @param {google.maps.LatLng} latlng - The LatLng object to extract coordinates from.
         */
        updateGeolocation: function (latlng) {
            document.getElementById(geolocationId).value = latlng.lat() + "," + latlng.lng();

            // Manually trigger a change event on the geolocation input
            var event = new Event('change', {bubbles: true});
            document.getElementById(geolocationId).dispatchEvent(event);
        },

        /**
         * Displays a temporary message in the message box.
         * @param {string} message - The message to display.
         * @param {string} type - 'info', 'warning', or 'error' to apply styling.
         */
        showMessage: function (message, type = 'info') {
            var messageBox = document.getElementById(messageBoxId);
            messageBox.textContent = message;

            // Clear previous styling classes
            messageBox.className = '';
            messageBox.classList.add('rounded-md', 'p-3', 'text-sm', 'font-medium', 'transition-opacity', 'duration-300', 'ease-in-out');

            // Apply type-specific styling
            if (type === 'error') {
                messageBox.classList.add('bg-red-100', 'text-red-800', 'border-red-400');
            } else if (type === 'warning') {
                messageBox.classList.add('bg-yellow-100', 'text-yellow-800', 'border-yellow-400');
            } else { // info
                messageBox.classList.add('bg-blue-100', 'text-blue-800', 'border-blue-400');
            }

            messageBox.classList.add('show'); // Make it visible

            // Hide the message after 5 seconds
            setTimeout(function () {
                messageBox.classList.remove('show');
            }, 5000);
        }
    };

    return self;
}

// Initialize the map when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    var googlemap = googleMapAdmin();
    googlemap.initialize();
});
