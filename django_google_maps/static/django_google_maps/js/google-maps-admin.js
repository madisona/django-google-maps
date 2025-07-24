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
                fullscreenControl: false,
                mapId: "dj-google-maps-admin"
            };

            // Create the map instance
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

            // If an existing location is present, set a marker
            if (existingLocation) {
                self.setMarker(latlng);
            }

            // Initialize Google Places Autocomplete Element
            const addressInput = document.getElementById(addressId);
            if (addressInput) {
                // Create the new Place Autocomplete web component
                autocomplete = new google.maps.places.PlaceAutocompleteElement();

                // Copy essential properties from the old input to the new element
                autocomplete.id = addressInput.id;
                autocomplete.name = addressInput.name;
                autocomplete.className = addressInput.className;
                autocomplete.placeholder = addressInput.placeholder || 'Enter an address';

                // *** THE FIX: Attach the element to the DOM *before* configuring it. ***
                // 1. Replace the original input with the new component.
                addressInput.parentNode.replaceChild(autocomplete, addressInput);

                // 2. Now that the element is live, apply Google-specific properties.
                const autocompleteOptions = self.getAutoCompleteOptions();
                if (autocompleteOptions.types) {
                    autocomplete.types = autocompleteOptions.types;
                }
                if (autocompleteOptions.componentRestrictions) {
                    autocomplete.componentRestrictions = autocompleteOptions.componentRestrictions;
                }

                // 3. Add the event listener.
                autocomplete.addEventListener("gmp-placechange", self.codeAddress);
            }
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
            // The original input is gone, so we get attributes from our new element.
            var autocompleteElement = document.getElementById(addressId);
            var autocompleteOptions = autocompleteElement.getAttribute('data-autocomplete-options');

            if (!autocompleteOptions) {
                return {
                    types: ['address']
                };
            }

            try {
                let parsedOptions = JSON.parse(autocompleteOptions);

                // Robustly cleanse the 'types' array for the old 'geocode' value.
                if (parsedOptions.types && Array.isArray(parsedOptions.types)) {
                    const typeIndex = parsedOptions.types.indexOf('geocode');
                    if (typeIndex > -1) {
                        console.warn(
                            "Google Maps Admin: The 'geocode' autocomplete type is deprecated for this component and was automatically replaced with 'address'. Please update the 'data-autocomplete-options' attribute in your HTML template."
                        );
                        parsedOptions.types[typeIndex] = 'address';
                    }
                }

                return parsedOptions;
            } catch (e) {
                console.error("Error parsing data-autocomplete-options:", e);
                self.showMessage("Error: Invalid autocomplete options format. Using default.", 'error');
                return {types: ['address']};
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
         * Geocodes the address from the autocomplete element.
         * Updates the map and marker based on the geocoded location.
         */
        codeAddress: function () {
            // For PlaceAutocompleteElement, the result is on the `.place` property
            var place = autocomplete.place;

            // Check if a place with geometry (location) was found
            if (place && place.geometry && place.geometry.location) {
                self.updateWithCoordinates(place.geometry.location);
            } else if (place && place.displayName) {
                // If no geometry, but a place name exists, try to geocode it.
                // The new Place object uses `displayName`.
                geocoder.geocode({'address': place.displayName}, function (results, status) {
                    if (status === 'OK' && results.length > 0) {
                        var latlng = results[0].geometry.location;
                        self.updateWithCoordinates(latlng);
                    } else if (status === 'ZERO_RESULTS') {
                        self.showMessage("No results found for '" + place.displayName + "'.", 'warning');
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
            var draggable = Options.draggable || false;
            marker = new google.maps.marker.AdvancedMarkerElement({
                map: map,
                position: Options.latlng,
                gmpDraggable: draggable
            });

            if (draggable) {
                self.addMarkerDrag(marker);
            }
        },

        /**
         * Adds a 'dragend' listener to the marker to update geolocation when dragged.
         */
        addMarkerDrag: function (draggableMarker) {
            // Use the modern addListener method
            draggableMarker.addListener('dragend', function (event) {
                self.updateGeolocation(event.latLng);
            });
        },

        /**
         * Updates the position of the existing marker.
         * @param {google.maps.LatLng} latlng - The new LatLng for the marker.
         */
        updateMarker: function (latlng) {
            marker.position = latlng;
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
            if (!messageBox) return; // Guard against missing message box
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

            messageBox.style.opacity = 1; // Make it visible

            // Hide the message after 5 seconds
            setTimeout(function () {
                messageBox.style.opacity = 0;
            }, 5000);
        }
    };

    return self;
}


async function initGoogleMap() {
    await google.maps.importLibrary("maps");
    await google.maps.importLibrary("marker");
    await google.maps.importLibrary("places");
    await google.maps.importLibrary("geocoding");

    var googlemap = googleMapAdmin();
    googlemap.initialize();
}