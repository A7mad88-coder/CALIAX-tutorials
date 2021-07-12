const mapboxgl = require('mapbox-gl');
const turf = require('@turf/turf')

console.log("Testtt")
mapboxgl.accessToken = '<MAPBOX API TOKEN>';
    var map = new mapboxgl.Map({
        container: 'map',
        // various map styles avaiable at https://docs.mapbox.com/api/maps/styles/#mapbox-styles
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [9.136786, 48.589326], //default
        zoom: 9
    });


    // Add geolocate control to the map.
    map.addControl(
        new mapboxgl.GeolocateControl({
        positionOptions: {
            enableHighAccuracy: true
        },
            trackUserLocation: true
        })
    );
    // 
    map.addControl(new mapboxgl.NavigationControl());
    var draw = new MapboxDraw({
        displayControlsDefault: false,
        controls: {
        polygon: true,
        trash: true
        }
    });
    map.addControl(draw);

    map.on('draw.create', updateArea);
    map.on('draw.delete', updateArea);
    map.on('draw.update', updateArea);

    function updateArea(e) {

        console.log("UpdateArea Fired ")

    }


    var marker = new mapboxgl.Marker({
        draggable: true
    })
    .setLngLat([9.136786, 48.589326])
    .addTo(map);
    
    function onDragEnd() {
        var lngLat = marker.getLngLat();
        coordinates.style.display = 'block';
        coordinates.innerHTML =
        'Longitude: ' + lngLat.lng + '<br />Latitude: ' + lngLat.lat;
        console.log('Longitude: ' + lngLat.lng + 'Latitude: ' + lngLat.lat);
        
        var data = draw.getAll();
        var pt = turf.point([lngLat.lng, lngLat.lat]);
        var polygonCoordinates = data['features'][0]['geometry']['coordinates'][0]
        // console.log("data: ", polygonCoordinates)
        geofenceStatus = turf.booleanPointInPolygon(pt, turf.polygon([polygonCoordinates]))
        console.log("GeoFence Status: ", geofenceStatus);
        var answer = document.getElementById('calculated-area');

        if (geofenceStatus) {
            answer.innerHTML = '<p>Device Inside Geofence</p>';
        } else {
            answer.innerHTML = '';
            answer.innerHTML = '<p>Device Outside Geofence</p>';
        }



    }
    
    marker.on('dragend', onDragEnd);