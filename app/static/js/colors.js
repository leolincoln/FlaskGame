
$(function() {
    console.log( "ready!" );
// haha as long as he pressed some key its gonna change color.
	//Red blue orange yellow green
		var colors=["rgba(255,0,0,0.5)","rgba(0,0,255,0.5)","rgba(255,165,0,0.7)","rgba(255,255,0,0.7)","rgba(0,128,0,0.5)"];
		var colors_string = ["Red","Blue","Orange","Yellow","Green"]

		//choose which color to use.
		var color_num = Math.floor((Math.random() * colors.length));

		//Have moved the constant setting for color div into css file.
		//$(".color").css("font-size","64").css("text-align","center");

		//Choose which text to use.
		var text_num = Math.floor((Math.random() * colors.length));
		$(".color").css("color",colors[color_num]).text(colors_string[text_num]);
    	$("body").focus();
		$("body").keypress(
	function(e){
		console.log( "keypressed" );
		if(correctKey(e)){
      console.log("in correctkey")
		var $this = $(this);
		var keyCounter = $this.data('keyCounter') || 0;
		keyCounter+=1;
		$this.data('keyCounter', keyCounter);
		console.log("key pressed "+keyCounter+" times.");

		//Red blue orange yellow green
		var colors=["rgba(255,0,0,0.5)","rgba(0,0,255,0.5)","rgba(255,165,0,0.7)","rgba(255,255,0,0.7)","rgba(0,128,0,0.5)"];
		var colors_string = ["Red","Blue","Orange","Yellow","Green"]
		//randomly select color to appear on screen
		var color_num = Math.floor((Math.random() * colors.length));
		var text_num = Math.floor((Math.random() * colors.length));
		$(".color").css("color",colors[color_num]).text(colors_string[text_num]);
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
function correctKey(e){

  var keycodes = [97,115,100,102,103];
	console.log(e.keyCode+" "+$.inArray(e.keyCode, keycodes));
	//var color = "rgba(0, 128, 0, 0.4)";
	if ($.inArray(e.keyCode, keycodes) !=-1){
    return true;
  }
	else {
    return false;
  }
	//red: 114 green 103, yellow 121, orange 111,blue 98
	}
