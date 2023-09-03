window.myNamespace = Object.assign({}, window.myNamespace, {
    mySubNamespace: {

        selectedMarker: null, // Keep track of the selected marker

        pointToLayer: function(feature, latlng, context) {
           //

            var defaultMarkerOptions = {
                radius: 15,
                weight: 1,
                color: 'blue',
                fillColor: 'blue',
                fillOpacity: 0.6
            };


            var selectedMarkerOptions = {
                radius: 25,
                weight: 2,
                color: 'red', // Change this to the desired selected color
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
         lineToLayer: function(feature, layer) {
            const props = feature.properties.regional_n;
            delete props.cluster;
            layer.bindPopup(JSON.stringify(props))

            layer.on('mouseover', function (e) {
                layer.setStyle({ color: 'red' , weight: 8});
                this.openPopup();
            });

            layer.on('mouseout', function (e) {
                layer.setStyle({ color: 'green', weight: 2 });
                this.closePopup();
            });

        }

    }

});

