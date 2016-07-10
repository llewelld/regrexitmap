var mymap = L.map('mapid').setView([54.505, -3.0], 6);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.emerald',
    accessToken: 'pk.eyJ1IjoiZmx5cGlnYWhveSIsImEiOiJjaXB3djc2cmgwMDZyaHRtMnh3b2F5aDRkIn0.OraLAjZ49vq0Z91NN5Pwhw'
}).addTo(mymap);

//mymap.on('click', onMapClick);
var areas = [];
$.getJSON( "data/change.js", function( data ) {
	areas = data;

	$.getJSON( "data/wpc-small-0.125.js", function( data ) {
		var myLayer = L.geoJson(null, {
			onEachFeature: function (feature, layer) {
				var id = feature.properties.PCON13CD;
				var info = "";
				var found = areas[id];
				var regrexit = (Math.round(found["change"] * 10.0) / 10.0);

				if (found != undefined) {
					info = found["name"] + "<br/>Remain: " + (Math.round(found["remain"] / (found["remain"] + found["leave"]) * 1000.0) / 10.0) + "%<br/>Regrexit: " + (Math.round(found["change"] * 10.0) / 10.0) + "<br/><img class=\"badge\" src=\"images/" + getbadge(regrexit) + "\"/>";
				}
				layer.bindPopup(info, {"minWidth": 160});
				
				// See http://palewi.re/posts/2012/03/26/leaflet-recipe-hover-events-features-and-polygons/
				(function(layer, properties) {
					layer.on("click", function(e) {
						var id = properties.PCON13CD;
						var found = areas[id];
						if (found != undefined) {
							var remain = (Math.round(found["remain"] / (found["remain"] + found["leave"]) * 1000.0) / 10.0)
							var leave = (Math.round(found["leave"] / (found["remain"] + found["leave"]) * 1000.0) / 10.0)
							var regrexit = (Math.round(found["change"] * 10.0) / 10.0);

							$("#pcon").html(found["name"]);
							$("#lad").html(found["loa"]);
							$("#mp").html(found["mp"]);
							$("#remain").html(found["remain"] + " (" + remain + "%)");
							$("#leave").html(found["leave"] + " (" + leave + "%)");
							$("#regrexit").html(regrexit);
							$("#sigs").html(found["sigs"]);
							$("#badge").attr("src", "images/" + getbadge(regrexit));
						}
					});
				})(layer, feature.properties);
			},
			style: function(feature) {
				var id = feature.properties.PCON13CD;
				var amount = areas[id]["change"];
				var shade = parseInt(amount * 128);
				if (shade > 255) {
					shade = 255;
				}

				component = shade.toString(16);
				if (shade < 16) {
					component = "0" + component;
				}
				anti = (255 - shade).toString(16);
				if ((255 - shade) < 16) {
					anti = "0" + anti;
				}

				color = "#" + component + component + anti;

				return {
					"color": "#0000ff",
					"weight": 2,
					"opacity": 0.5,
					"fillColor": color,
					"fillOpacity": 0.25
				}
			}
		}).addTo(mymap);
		myLayer.addData(data);

		showLoading(false);

	})
	.fail(function( jqxhr, textStatus, error ) {
		showError(true, "Failed to load boundary data");
	});
})
.fail(function( jqxhr, textStatus, error ) {
	showError(true, "Failed to load statistics");
});

function showLoading(show) {
	if (show) {
		$("#loading").html("<h1>Loading</h1><p/>Please wait...<span>");
		$("#loading").show(0);
	}
	else {
		$("#loading").hide(0);
	}
}

function showError(show, message) {
	if (show) {
		$("#loading").html("<h1>Error</h1><p/>" + message + "<span>");
		$("#loading").show(0);
	}
	else {
		$("#loading").hide(0);
	}
}

function getbadge(regrexit) {
	var image = "none.png"
	if (regrexit < 0.8) {
		image = "consolidate.png";
	}
	else if (regrexit <= 1.2) {
		image = "accept.png";
	}
	else {
		image = "regret.png";
	}
	return image;
}

function getsigcount(id) {
	var count = 0;
	var found = areas.find(function(element, index, array) {
		return element["ons_code"] == id;
	});
	if (found != undefined) {
		count = found["signature_count"];
	}
	return count;
}



