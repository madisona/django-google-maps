
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

    var geocoder = new google.maps.Geocoder();
    var map;
    var marker;

    var self = {
        initialize: function() {
            var lat = 0;
            var lng = 0;
            var zoom = 2;
            // set up initial map to be world view. also, add change
            // event so changing address will update the map
            existinglocation = self.getExistingLocation();
            if (existinglocation) {
                lat = existinglocation[0];
                lng = existinglocation[1];
                zoom = 18;
            }else{
                self.getHtml5Location();
            }

            var latlng = new google.maps.LatLng(lat,lng);
            var myOptions = {
              zoom: zoom,
              center: latlng,
              mapTypeId: google.maps.MapTypeId.HYBRID
            };
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
            if (existinglocation) {
                self.setMarker(latlng);
            }

            google.maps.event.addListener(map, 'click', function(new_location) {
                self.updateGeolocation(new_location.latLng);
                self.setMarker(new_location.latLng);
                self.codeLocation(new_location.latLng);
            });

            $("#id_address").change(function() {self.codeAddress();});
        },


        getHtml5Location: function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(self.updateHtml5Location);
            }

        },

        updateHtml5Location: function(position) {
            var latLng = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
            self.updateGeolocation(latLng);
            self.setMarker(latLng);
            self.codeLocation(latLng);
            map.setCenter(latLng);
            map.setZoom(18);
        },


        getExistingLocation: function() {
            var geolocation = $("#id_geolocation").val();
            if (geolocation && geolocation !== '0,0') {
                return geolocation.split(',');
            }
        },

        codeAddress: function() {
            var address = $("#id_address").val();

            if ( $("#id_address").data("addrtype") === "simple"){
            
                if( $('#id_postalcode').length )
                {
                    address = address + " " + $("#id_postalcode").val()
                }

                if( $('#id_city').length )
                {
                    address = address + " " + $("#id_city").val()
                }

            }

            address = address.trim()

            geocoder.geocode({'address': address}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var latlng = results[0].geometry.location;
                    map.setCenter(latlng);
                    map.setZoom(18);

                    self.setMarker(latlng);
                    self.updateGeolocation(latlng);
                } else {
                    alert("Geocode was not successful for the following reason: " + status);
                }
            });
        },

        codeLocation: function(latlng) {

            geocoder.geocode({'latLng': latlng}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    if (results[0]) {
                        var street_number = "";
                        var street_name = "";

                        for (var i = 0; i < results[0].address_components.length; i++) { 
                            
                            if (results[0].address_components[i].types.indexOf('street_number')>= 0){
                                street_number = ", "+ results[0].address_components[i].long_name;
                            }

                            if (results[0].address_components[i].types.indexOf('route')>= 0){
                                street_name = results[0].address_components[i].long_name;
                            }

                            if (results[0].address_components[i].types.indexOf('locality')>= 0){
                                if( $('#id_city').length )
                                {
                                    $("#id_city").val(results[0].address_components[i].long_name);
                                }
                            }

                            if (results[0].address_components[i].types.indexOf('postal_code')>= 0){
                                if( $('#id_postalcode').length )
                                {
                                    $("#id_postalcode").val(results[0].address_components[i].long_name);
                                }
                            }

                            if (results[0].address_components[i].types.indexOf('administrative_area_level_2')>= 0){
                                if( $('#id_adminarea2').length )
                                {
                                    $("#id_adminarea2").val(results[0].address_components[i].long_name);
                                }
                            }

                            if (results[0].address_components[i].types.indexOf('administrative_area_level_1')>= 0){
                                if( $('#id_adminarea1').length )
                                {
                                    $("#id_adminarea1").val(results[0].address_components[i].long_name);
                                }
                            }

                            if (results[0].address_components[i].types.indexOf('country')>= 0){
                                if( $('#id_country').length )
                                {
                                    $("#id_country").val(results[0].address_components[i].long_name);
                                }
                            }
                        }

                        if ( $("#id_address").data("addrtype") === "simple"){
                        
                            $("#id_address").val(street_name + street_number);
                        
                        }else{
                            $("#id_address").val(results[0].formatted_address);
                        }


                    }else{
                        alert("Geocode was not successful. No address found.");
                    }
                } else {
                    alert("Geocode was not successful for the following reason: " + status);
                }
            });
        },

        setMarker: function(latlng) {
            if (marker) {
                self.updateMarker(latlng);
            } else {
                self.addMarker({'latlng': latlng, 'draggable': true});
            }
        },

        addMarker: function(Options) {
            marker = new google.maps.Marker({
                map: map,
                position: Options.latlng
            });

            var draggable = Options.draggable || false;
            if (draggable) {
                self.addMarkerDrag(marker);
            }
        },

        addMarkerDrag: function() {
            marker.setDraggable(true);
            google.maps.event.addListener(marker, 'dragend', function(new_location) {
                self.updateGeolocation(new_location.latLng);
            });
        },

        updateMarker: function(latlng) {
            marker.setPosition(latlng);
        },

        updateGeolocation: function(latlng) {
            $("#id_geolocation").val(latlng.lat() + "," + latlng.lng());
        }
    }

    return self;
}

$(document).ready(function() {
    var googlemap = googleMapAdmin();
    googlemap.initialize();
});