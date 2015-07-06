
$(function() {
    console.log( "ready!" );
// haha as long as he pressed some key its gonna change color. 
$("body").focus();
$("body").keypress(
	function(e){
		console.log( "keypressed" );
		if(correctKey($(".color").css("background-color"),e)){
		var $this = $(this);
		var keyCounter = $this.data('keyCounter') || 0;
		keyCounter+=1;
		$this.data('keyCounter', keyCounter);
		console.log("key pressed "+keyCounter+" times.");
		
		//Red blue orange yellow green 
		var colors=["rgba(255,0,0,0.5)","rgba(0,0,255,0.5)","rgba(255,165,0,0.7)","rgba(255,255,0,0.7)","rgba(0,128,0,0.5)"];

		//randomly select color to appear on screen. 
		$(".color").css("background-color",colors[Math.floor((Math.random() * colors.length))]);
    $("body").focus();
		if(keyCounter>10){
			var currLocation =window.location.href;
			var add = window.location.href.split("\/");
			var newLocation = currLocation.substring(0,currLocation.length-add[add.length-1].length)+"chat";
			window.location.href=newLocation;
		}
	}
		//console.log(e);
	});
});
/**
	Args: 
		color: String of background-color in css of this element
		e: the keypress event
*/
function correctKey(color,e){
	red = "255, 0, 0";
	blue="0, 0, 255";
	orange="255, 165, 0";
	yellow="255, 255";
	green="0, 128, 0";
	console.log(color);
	console.log(color.indexOf(red));
	//var color = "rgba(0, 128, 0, 0.4)";
	if(color.indexOf(red)!=-1 && e.keyCode==114) return true;
	else if(color.indexOf(blue)!=-1 && e.keyCode==98) return true;
	else if(color.indexOf(orange)!=-1 && e.keyCode==111) return true;
	else if(color.indexOf(yellow)!=-1 && e.keyCode==121) return true;
	else if(color.indexOf(green)!=-1 && e.keyCode==103) return true;
	else return false;
	//red: 114 green 103, yellow 121, orange 111,blue 98
	}
