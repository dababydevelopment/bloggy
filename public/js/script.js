document.getElementById("theme-toggle").addEventListener("change", function() {
    document.body.classList.toggle("light-theme");
    document.body.classList.toggle("dark-theme");
  });  

var i = 0;
if (screen.width <= 500) {
	document.getElementById("sidebar-container").classList.toggle("visible");
	document.getElementById("content").style.paddingLeft = "0";
	i = 1
}
function sidebar() {
	i++;

	document.getElementById("lineTop2").style.transform = "rotate(45deg)";
	document.getElementById("lineTop2").style.top = "5px";
	document.getElementById("lineBottom2").style.transform = "rotate(-45deg)";
	document.getElementById("lineBottom2").style.bottom = "5px";

	document.getElementById("lineTop1").style.transform = "rotate(45deg)";
	document.getElementById("lineTop1").style.top = "5px";
	document.getElementById("lineBottom1").style.transform = "rotate(-45deg)";
	document.getElementById("lineBottom1").style.bottom = "5px";


	if (i % 2 == 0) {
		setTimeout(() => { 
		document.getElementById("content").style.paddingLeft = "230px";

			document.getElementById("sidebar-container").classList.toggle("visible");		
		}, 300);
	} else {

		document.getElementById("content").style.paddingLeft = "0";

		document.getElementById("lineTop2").style.transform = "rotate(0)";
		document.getElementById("lineTop2").style.top = "0";
		document.getElementById("lineBottom2").style.transform = "rotate(0)";
		document.getElementById("lineBottom2").style.bottom = "0";

		document.getElementById("lineTop1").style.transform = "rotate(0)";
		document.getElementById("lineTop1").style.top = "0";
		document.getElementById("lineBottom1").style.transform = "rotate(0)";
		document.getElementById("lineBottom1").style.bottom = "0";


		setTimeout(() => { 
			document.getElementById("sidebar-container").classList.toggle("visible");		
		}, 100);
	}
}
