$(document).ready(function(){  


// help tooltip

	$("div#ver-help").hide();

	$("img#ver-help-trigger").hover( 
		function() {
			$("div#ver-help").fadeIn("slow");
		},
		function() {
			$("div#ver-help").fadeOut("slow");
		}
	);
});

