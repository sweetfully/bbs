$(document).ready(function(){
	$("#gz_ph_xz").mouseenter(function() {
		$("#gz_phb").show();
		$("#dz_phb").hide();
		$("#gz_ph_xz").css("background-color","#F5F5F5")
		$("#dz_ph_xz").css("background-color","#fff")
	});

	$("#dz_ph_xz").mouseenter(function() {
		$("#gz_phb").hide();
		$("#dz_phb").show();
		$("#gz_ph_xz").css("background-color","#fff")
		$("#dz_ph_xz").css("background-color","#F5F5F5")
	});
});
