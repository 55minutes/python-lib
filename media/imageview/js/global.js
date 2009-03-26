function blurAnchors() {
  if(document.getElementsByTagName) {
    var a = document.getElementsByTagName("a");
    for(var i = 0; i < a.length; i++) {
      a[i].onfocus = function(){this.blur()};
    }
  }
}

function externalLinks() {
	if (!document.getElementsByTagName) return;
	var anchors = document.getElementsByTagName("a");
	for (var i=0; i<anchors.length; i++) {
		var anchor = anchors[i];
		if (anchor.getAttribute("href") &&
			anchor.getAttribute("rel") == "external")
		anchor.target = "_blank";
	}
}

function sw(object){
		document.getElementById(object).style.display="block";
}

window.onload = function() {
	fadeabout = new fx.Height('aboutinfo', {duration: 400}); fadeabout.hide('height');

	blurAnchors();
	externalLinks();
}
