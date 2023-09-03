window.myNamespace = Object.assign({}, window.myNamespace, {
    mySubNamespace: {

        selectedMarker: null, // Keep track of the selected marker
        selectedLineMarker: null,



        pointToLayer: function(feature, latlng, context) {


           //

            var defaultMarkerOptions = {
                radius: 15,
                weight: 4,
                color: 'orange',
                fillColor: 'blue',
                fillOpacity: 0.6
            };


            var selectedMarkerOptions = {
                radius: 25,
                weight: 4,
                color: 'orange', // Change this to the desired selected color
                fillColor: 'red', // Change this to the desired selected color
                fillOpacity: 0.7
            };


            var marker = L.circleMarker(latlng, defaultMarkerOptions);


            // Extract relevant properties (change 'property1' and 'property2' to actual property names)
            var property1 = feature.properties.sur_unit;


            // Construct popup content using extracted properties
            var popupContent = property1;

            marker.bindPopup(popupContent);

            marker.on('mouseover', function (e) {
                this.openPopup();
            });

            marker.on('mouseout', function (e) {
                this.closePopup();
            });

            marker.on('click', function (e) {
                if (window.myNamespace.mySubNamespace.selectedMarker) {
                    console.log('Clicked')
                    console.log(property1)


                    // Reset the style of the previously selected marker
                    window.myNamespace.mySubNamespace.selectedMarker.setStyle(defaultMarkerOptions);
                }

                if (window.myNamespace.mySubNamespace.selectedMarker !== this) {
                    // Change the style of the newly selected marker
                    this.setStyle(selectedMarkerOptions);
                    window.myNamespace.mySubNamespace.selectedMarker = this;
                } else {
                    // Clear the selection
                    window.myNamespace.mySubNamespace.selectedMarker = null;
                }
            }


            );

            return marker;

        },
         lineToLayer: function (feature, layer) {
    // Define default marker options
    var defaultMarkerOptions = {
        weight: 8,
        color: 'green',
    };

    // Define selected marker options (change color as needed)
    var selectedMarkerOptions = {
        weight: 10,
        color: 'red', // Change this to the desired selected color
    };

    // Store the layer in a marker variable
    var marker = layer;

    // Extract the 'regional_n' property from the feature
    var property1 = feature.properties.regional_n;

    // Remove the 'cluster' property from property1 if it exists
    delete property1.cluster;

    // Construct popup content using extracted properties
    var popupContent = property1;
    layer.bindPopup(JSON.stringify(property1));

    // Attach event handlers for mouse interactions
    marker.on('mouseover', function (e) {
        this.openPopup();
    });

    marker.on('mouseout', function (e) {
        this.closePopup();
    });

    marker.on('click', function (e) {
        if (window.myNamespace.mySubNamespace.selectedLineMarker) {
            console.log('Clicked');
            console.log(property1);

            // Reset the style of the previously selected marker
            window.myNamespace.mySubNamespace.selectedLineMarker.setStyle(defaultMarkerOptions);
        }

        if (window.myNamespace.mySubNamespace.selectedLineMarker !== this) {
            // Change the style of the newly selected marker
            this.setStyle(selectedMarkerOptions);
            window.myNamespace.mySubNamespace.selectedLineMarker = this;
        } else {
            // Clear the selection
            window.myNamespace.mySubNamespace.selectedLineMarker = null;
        }
    });

    return marker;
},



    }

});

