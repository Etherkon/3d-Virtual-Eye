// Some helpers for the UI

function displayDate()
{
    var currentTime = new Date();
    var month = currentTime.getMonth() + 1;
    var day = currentTime.getDate();
    var year = currentTime.getFullYear();
    document.write(day + "/" + month + "/" + year);
}
 
function displayTime()
{
    var currentTime = new Date()
    var hours = currentTime.getHours()
    var minutes = currentTime.getMinutes()
    if (minutes < 10){
        minutes = "0" + minutes
    }
    document.write(hours + ":" + minutes + " ")
    if(hours > 11){
        document.write("PM")
    } else {
        document.write("AM")
    }
}
