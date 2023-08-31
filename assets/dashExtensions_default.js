window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, layer, context) {
            if (feature.properties.sur_unit) { // don't bind anything for clusters (that do not have a city prop)
                layer.bindTooltip(`${feature.properties.sur_unit})`)
            }
        },
        function1: function(feature, latlng, context) {

            var defaultMarkerOptions = {
                radius: 10,
                weight: 1,
                color: 'blue',
                fillColor: 'blue',
                fillOpacity: 0.6
            };
            var marker = L.circleMarker(latlng, defaultMarkerOptions);
            return marker;; // render a simple circle marker
        }
    }
});