// Create new websocket on given server (There was no routing done by Apache, so the IP had to be present)
ws = new WebSocket("ws://192.168.10.101:8888/wsmain")

// This is for updating the Simcore image
window.pic_number = 0

// Whenever new Websocket connection has been created
ws.onopen = function() {
//	ws.send("position 61.4972 23.749")
	// For some reason getting image size didn t work universally
	//ws.send("image_size " +  document.getElementById("cigi_image").clientWidth + " " + document.getElementById("cigi_image").clientHeight)
	ws.send("image_size 552 344")
	// Set current time
	ws.send("time")
	// And weather
	ws.send("weather now")
}

// Whenever we receive a message
ws.onmessage = function(evt) {
	if( evt.data == "screenshotted" ){
		// Image has been updated, fetch the new one
		updateImage()
	}
	// We also receive clicked entityID -message but it s ignored
}

// Funciton to add objects to SimCore
function addObjects(type, coordinates) {
	ws.send( create + type + coordinates )
}

// To tell browser to force refresh image on page
function updateImage()
{
	// Image ain t updated unless the n parameter changes
	document.getElementById("cigi_image").src = "/images/SimCore_screenshot.png?n=" + window.pic_number;
	//alert("Image updated");
	// Update the pic number and check for overflow
	window.pic_number = window.pic_number + 1;
	if( window.pic_number == 32765 ){
		window.pic_number = 0
	}
	// Without websockets we could use recursion and timer
//	setTimeout("updateImage(" + pic_number + ")", 1000);
}

// Check if HTML5 Geolocation is supported
if (navigator.geolocation)
{
	//If the browser supports geolocation
	navigator.geolocation.getCurrentPosition(geoloc_success, geoloc_error);
} 
else
{
	//Browser does not support geolocation
	error('HTML5 Geolocation not supported');
	window.ws.send( "error Geolocation not supported by client" )
}

var service 

function geoloc_success(position)
{
	// console.log(position.coords.latitude)
	// console.log(position.coords.longitude)
	// console.log(position.coords.altitude)
	// console.log(position.coords.accuracy)
	// console.log(position.coords.altitudeAccuracy)
	// console.log(position.coords.heading)
	// console.log(position.coords.speed)
	// Geolocation successful
	setposition(position.coords.latitude, position.coords.longitude)

}

// Tells server to reposition us to given location
function setposition(lat, lng) {
	window.ws.send("position " + lat + " " + lng )

	// Set up Google Maps
	var latlng = new google.maps.LatLng(lat, lng)

	// Request for Google Places API
	var request = {
		location: latlng,
		radius: '1500',
		types: ['restaurant','cafe','bar']
	};

	// Some required options
	var myOptions = {
		zoom: 15,
		center: latlng,
		mapTypeControl: false,
		navigationControlOptions: {style: google.maps.NavigationControlStyle.SMALL},
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	// Query doesn t work without Google Maps
	var mapcanvas = document.createElement('div');
	mapcanvas.id = 'mapcanvas';
	mapcanvas.style.height = '0px';
	mapcanvas.style.width = '0px';
	
	document.querySelector('article').appendChild(mapcanvas);

	// Create the map
	map = new google.maps.Map(document.getElementById("mapcanvas"), myOptions);	

	// Create the service using given map information
	service = new google.maps.places.PlacesService(map);
	// Do the actual query
	service.search(request, placesSuccess);	
}

function geoloc_error(error)
{
	console.log( "Geolocation error")
	// We ll set up default position anyways because Safari fails for unknown reason
	setposition(61.497978, 23.764931)	
	switch(error.code)
	{
		case error.TIMEOUT:
			window.ws.send("error geolocation timeout")
			break
		case error.POSITION_UNAVAILABLE:
			window.ws.send("error geolocation pos unavailable")
			break
		case error.PERMISSION_DENIED:
			window.ws.send("error client denied geolocation")
			alert("GPS location denied")
			break
		case error.UNKNOWN_ERROR:
			window.ws.send("error Unknown")
			break
	}

}

function move(direction)
{
	// Tell server to move us to given direction
	window.ws.send("move " + direction)
}

function placesSuccess(results, status) 
{
	if (status == google.maps.places.PlacesServiceStatus.OK) // if the places have been found?
	{
		var id = 10
		var place = results[0];
		//for (var i = 0; i < results.length; i++) 
		var allRestCoor = "";
		for (var i = 0; i < results.length; i++) 
		{
			place = results[i];
			//createMarker(place); 
			
			// This puts all the restaurant coordinates in one string, separating them with ;
			allRestCoor += place.geometry.location.lat() + 
							"," + 
							place.geometry.location.lng() + 
							"," + id + " ";
//			ws.send("create " + place.types[0] + " " + place.geometry.location.lat() + " " + place.geometry.location.lng() + " " + id)
			id = id + 1

		}
		// The string holding the coordinates are sent to the function that communicates with the python server
	//	addObject2Cigi(allRestCoor);
	ws.send("multicreate restaurant " + allRestCoor )
	}
}
