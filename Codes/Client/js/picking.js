//<!-- Used to get coordinates of the event on some image  -->
// Was not actually used in the demo but should work
function clicked_img(event)
{
	// ARGH... Works only in Chrome and Safari?
	var img = document.getElementById("cigi_image")
	pos_x = event.offsetX?(event.offsetX):event.pageX-img.offsetLeft;
	pos_y = event.offsetY?(event.offsetY):event.pageY-img.offsetTop;

	//for Firefox
	if( img.offsetLeft == 0 ) {
		var top = 0, left = 0;
		var elm = img;
		while (elm) {
			left += elm.offsetLeft;
			top += elm.offsetTop;
			elm = elm.offsetParent;
		}

		pos_x = event.pageX-left;
		pos_y = event.pageY-top;
	}

	// Log some info to get information about which things were supported
	console.log( event.offsetX + " vs. " + event.pageX + " vs. " + img.offsetLeft)
	// Make the click relative to the center of the image
	pos_x = pos_x - img.clientWidth/2
	pos_y = pos_y - img.clientHeight/2
	// Send query to server
	window.ws.send("clicked " + pos_x + " " + pos_y)
}