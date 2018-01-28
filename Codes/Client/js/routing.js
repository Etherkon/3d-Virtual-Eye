// Bulletproof way to route clicks on elements to Websocket
document.getElementById("zoomIn").onclick = function() {
	move("street")
}

document.getElementById("zoomOut").onclick = function() {
	move("tosky")
}


// Except in this case, because the image gets refreshed or something
//document.getElementById("cigi_image").onclick = clicked_img(event)

document.getElementById("leftView").onclick = function() {
	move("left")
}

document.getElementById("rightView").onclick = function() {
	move("right")
}

document.getElementById("upView").onclick = function() {
	move("forward")
}

document.getElementById("downView").onclick = function() {
	move("backward")
}

// document.getElementById("summermode").onclick = function() {
//	console.log("S")
//}

//document.getElementById("wintermode").onclick = function() {
//	console.log("W")
//}

