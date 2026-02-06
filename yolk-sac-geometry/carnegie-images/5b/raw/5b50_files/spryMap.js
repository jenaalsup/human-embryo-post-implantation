/**
* http://candrews.net/blog/2010/10/introducing-sprymap/
* Charlie Andrews
*
* Instantiate the widget when you want it to turned into a map,
* probably in the window.onload or $(document).ready() function.
*
* Default parameters are listed as the parameters below
* var map = new spryMap({
* // The ID of the element being transformed into a map
* id : "",
* // The width of the map (in px)
* width: 800,
* // The height of the map (in px)
* height: 800,
* // The X value of the starting map position
* startX: 0,
* // The Y value of the starting map position
* startY: 0,
* // Boolean true if the map should animate to a stop
* scrolling: true,
* // The time (in ms) that the above scrolling lasts
* scrollTime: 300,
* // Boolean true if the map disallows moving past its edges
* lockEdges: true,
* // The CSS class attached to the wrapping map div
* cssClass: ""
* });
*
*/


var cD = "url(data:image/x-win-bitmap;base64,AAACAAEAICACAAcABQAwAQAAFgAAACgAAAAgAAAAQAAAAAEAAQAAAAAAAAEAAAAAAAAAAAAAAgAAAAAAAAAAAAAA////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD8AAAA/AAAAfwAAAP+AAAH/gAAB/8AAAH/AAAB/wAAA/0AAANsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//////////////////////////////////////////////////////////////////////////////////////gH///4B///8Af//+AD///AA///wAH//+AB///wAf//4AH//+AD///yT/////////////////////////////8=), url(/images/grab2.cur), default";

var cU = "url(data:image/x-win-bitmap;base64,AAACAAEAICACAAcABQAwAQAAFgAAACgAAAAgAAAAQAAAAAEAAQAAAAAAAAEAAAAAAAAAAAAAAgAAAAAAAAAAAAAA////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD8AAAA/AAAAfwAAAP+AAAH/gAAB/8AAA//AAAd/wAAGf+AAAH9gAADbYAAA2yAAAZsAAAGbAAAAGAAAAAAAAA//////////////////////////////////////////////////////////////////////////////////////gH///4B///8Af//+AD///AA///wAH//4AB//8AAf//AAD//5AA///gAP//4AD//8AF///AB///5A////5///8=), url(/images/grab3.cur), default";

function SpryMap(c) {

    function g(b,e) {
        var d = b, f = e
        if (a.lockEdges) {
            var j = -a.map.offsetWidth+a.viewingBox.offsetWidth/2,
            k = -a.map.offsetHeight+a.viewingBox.offsetHeight/2;
            d = d < j ? j : d;
            f = f < k ? k : f;
            d = d > a.viewingBox.offsetWidth/2 ? a.viewingBox.offsetWidth/2 : d;
            f = f > a.viewingBox.offsetHeight/2 ? a.viewingBox.offsetHeight/2: f
        }
        a.map.style.left = d + "px";
        a.map.style.top = f + "px"
    }

    function h(b,e,d) {
        if (b.attachEvent) {
            b["e"+e+d] = d;
            b[e+d] = function() {
                b["e"+e+d](window.event)
            };
            b.attachEvent("on"+e,b[e+d])
        } else b.addEventListener(e,d,false)
    }
    function i(b,e) {
        this.x = b;
        this.y = e
    }

    var a = this;
    a.map = document.getElementById(c.id);
    a.width = typeof c.width == "undefined" ? 800 : c.width;
    a.height = typeof c.height == "undefined" ? 800 :c.height;
    a.scrolling = typeof c.scrolling == "undefined" ? true : c.scrolling;
    a.scrollTime = typeof c.scrollTime == "undefined" ? 300 : c.scrollTime;
    a.lockEdges = typeof c.lockEdges == "undefined" ? true : c.lockEdges;
    a.viewingBox = document.createElement("div");
    if (typeof c.cssClass!="undefined") a.viewingBox.className=c.cssClass;
    a.mousePosition=new i;a.mouseLocations=[];
    a.velocity=new i;
    a.mouseDown=false;
    a.timerId=-1;
    a.timerCount=0;
    a.map.parentNode.replaceChild(a.viewingBox,a.map);

    a.viewingBox.appendChild(a.map);
    a.viewingBox.style.overflow="hidden";
    a.viewingBox.style.width=a.width+"px";
    a.viewingBox.style.height=a.height+"px";
    a.viewingBox.style.position="relative";
    a.map.style.position="absolute";
	if (mode == 'ruler') {
		a.viewingBox.style.cursor='crosshair';
	} else {
		a.viewingBox.style.cursor=cU;
	}
    g(typeof c.startX=="undefined"?0:-c.startX,typeof c.startY=="undefined"?0:-c.startY);

    mouseMove=function(b) {
        var e=b.clientX-a.mousePosition.x+parseInt(a.map.style.left),d=b.clientY-a.mousePosition.y+parseInt(a.map.style.top);

		if (mode=="ruler") {
			if (!rulerstarted) return;
			var ruler = document.getElementById('ruler');
			var ruler1 = document.getElementById('ruler1');
			var rulernum = document.getElementById('rulernum');
			var x = b.clientX - $('#slpic').offset().left + $(window).scrollLeft();
			var y = b.clientY - $('#slpic').offset().top + $(window).scrollTop();
			var w = x - rulerstartx;
			var h = y - rulerstarty;
		
			//if (w < -rulerstartx) w = -rulerstartx;
			//if (w > viewing_width - rulerstartx) w = viewing_width - rulerstartx;
			//if (h < -rulerstarty) h = -rulerstarty;
			//if (h > viewing_height - rulerstarty) h = viewing_height - rulerstarty;
		
			var rad = Math.atan(h/w);
			if (isNaN(rad)) return;
			
			var angle = rad / Math.PI * 180;
			var costheta = Math.cos(rad);
			var sintheta = Math.sin(rad);
			var length = Math.sqrt(w*w + h*h);
			var xoff = -3;
			var yoff = -9;
		
			if (document.all && !window.opera && !window.atob) {
				ruler1.filters.item(0).M11 = costheta;
				ruler1.filters.item(0).M12 = -sintheta;
				ruler1.filters.item(0).M21 = sintheta;
				ruler1.filters.item(0).M22 = costheta;
		
				xoff += -7.5*Math.abs(sintheta);
				yoff += 3 - 7.5*Math.abs(costheta);
			} else {
				$("#ruler1").css({
					'transform': 'rotate('+angle+'deg)',
					'-moz-transform': 'rotate('+angle+'deg)',
					'-o-transform': 'rotate('+angle+'deg)',
					'-webkit-transform': 'rotate('+angle+'deg)'
				});
				xoff += (costheta-1) * length / 2;
				yoff += Math.abs(h)/2;
			}
		
			if (w > 0) {
				ruler.style.left = (rulerstartx+xoff)+"px";
				ruler.style.width = w+"px";
			} else {
				ruler.style.left = (rulerstartx+w+xoff)+"px";
				ruler.style.width = (-w)+"px";
			}
			ruler1.style.width = length+"px";
			if (h > 0) {
				ruler.style.top = (rulerstarty+yoff)+"px";
				ruler.style.height = h+"px";
			} else {
				ruler.style.top = (rulerstarty+h+yoff)+"px";
				ruler.style.height = (-h)+"px";
			}
			ruler.style.display = 'block';
			
			var microns = slide.um_per_pixel * length;
			microns = microns.toPrecision(3);
			if (microns >= 1000) {
				microns = (microns/1000) + " mm";
			} else {
				microns = microns + " μm"	
			}
			rulernum.innerHTML = microns;
			rulernumx = "50";
			rulernum.style.left = (rulerstartx+(w<0?w:0) + Math.abs(w)/2 - 30 - 42*sintheta) + "px";
			rulernum.style.top = (rulerstarty+(h<0?h:0) + Math.abs(h)/2 - 10 + 21*costheta) + "px";
			rulernum.style.display = 'block';
	
			if (document.selection) {
				document.selection.empty();
			} else {
				window.getSelection().removeAllRanges();
			}
		
		} else {
        	g(e,d);
		}
		
		a.mousePosition.x=b.clientX;
        a.mousePosition.y=b.clientY
    };

    onTimer=function() {
        if(a.mouseDown) {
            a.mouseLocations.unshift(new i(a.mousePosition.x,a.mousePosition.y));
            a.mouseLocations.length > 10 && a.mouseLocations.pop()
        } else {
            var b=a.scrollTime/20,e=a.velocity.y*((b-a.timerCount)/b);
            g(-(a.velocity.x*((b-a.timerCount)/b))+parseInt(a.map.style.left),-e+parseInt(a.map.style.top));
            if(a.timerCount==b) {
                clearInterval(a.timerId);
                a.timerId=-1
            }
            ++a.timerCount
        }
    };

    h(a.viewingBox, "mousedown", function(b) {
		if (mode == 'ruler') {
			rulerstarted = true;
			rulerstartx = b.clientX - $('#slpic').offset().left + $(window).scrollLeft();
			rulerstarty = b.clientY - $('#slpic').offset().top + $(window).scrollTop();
			$("#ruler").css("display","");
			$("#rulernum").css("display","");
			a.viewingBox.style.cursor='url(/images/blank.cur), none';
		} else {
			a.viewingBox.style.cursor=cD;
		}

        a.timerId!=-1 && a.scrolling && clearInterval(a.timerId);
        a.mousePosition.x=b.clientX;
        a.mousePosition.y=b.clientY;
        h(document,"mousemove",mouseMove);
        a.mouseDown=true;
        if(a.scrolling) {
            a.timerCount=0;
            a.timerId=setInterval("onTimer()",20)
        }
		b.returnValue = false;
		if (b.stopPropagation) b.stopPropagation(); 
    });

    h(document, "mouseup", function() {
        if(a.mouseDown) {
            var b=mouseMove;
            if(document.detachEvent) {
                document.detachEvent("onmousemove",document["mousemove"+b]);
                document["mousemove"+b]=null
            } else document.removeEventListener("mousemove",b,false);a.mouseDown=false;
            if(a.mouseLocations.length>0) {
                b=a.mouseLocations.length;
                a.velocity.x=(a.mouseLocations[b-1].x-a.mouseLocations[0].x)/b;
                a.velocity.y=(a.mouseLocations[b-1].y-a.mouseLocations[0].y)/b;
                a.mouseLocations.length=0
            }
        }
		if (mode == "ruler") {
			rulerstarted = false;
			a.viewingBox.style.cursor='crosshair';
		} else {
			a.viewingBox.style.cursor=cU;
		}
    })
};

var rulerstartx, rulerstarty, rulerstarted=false;

function togglekey() {
	var key = document.getElementById("labelkey");
	if (key.style.display == 'none') key.style.display = '';
	else key.style.display = 'none';
	return false;	
}

function togglelabel(is_on) {
	if (is_on) {
		$("#labelon").css("display", "");
		$("#labeloff").css("display", "none");
		$("#labelvis").css("display", "");
	} else {
		$("#labelon").css("display", "none");
		$("#labeloff").css("display", "");
		$("#labelvis").css("display", "none");
	}
	labels = is_on;
	$.ajax({url:'drem_slide_json.php', data:{"stage":slide.stage,"section":slide.section,"zoom":slide.zoom,"labels":is_on}});
	return false;	
}

var slide_archive = {};
function updateslide(key, value, key2, value2) {
	if (key2) {
		if (slide[key] == value && slide[key2] == value2 ) return false;
		slide[key2] = value2;
	} else {
		if (slide[key] == value) return false;
	}
	slide[key] = value;
	if (key == 'zoom' || key == 'stage' || key2 == 'stage') {
		$("#ruler").css("display","none");
		$("#rulernum").css("display","none");
	}
	if (key == 'stage') {
		slide.section = 0;
	}
	if (slide_archive[slide.zoom] && slide_archive[slide.zoom][slide.stage] && slide_archive[slide.zoom][slide.stage][slide.section]) {
		var w = slide.width;
		var h = slide.height;
		var copy = {};
		for (x in slide_archive[slide.zoom][slide.stage][slide.section]) {
			if (slide_archive[slide.zoom][slide.stage][slide.section].hasOwnProperty(x)) {
				copy[x] = slide_archive[slide.zoom][slide.stage][slide.section][x];
			}
		}
		slide = copy;
		
		readslide(w, h);	
	} else {
		$.ajax({url:'drem_slide_json.php', data:{stage:slide.stage, section:slide.section, percent:slide.percent, zoom:slide.zoom, labels:labels}, success:finish_slide_json});
	}
	return false;
}

function finish_slide_json(data) {
	var w = slide.width;
	var h = slide.height;
	
	slide = jQuery.parseJSON(data);
	if (!slide_archive[slide.zoom]) slide_archive[slide.zoom] = {};
	if (!slide_archive[slide.zoom][slide.stage]) slide_archive[slide.zoom][slide.stage] = {};
	slide_archive[slide.zoom][slide.stage][slide.section] = {};
	for (x in slide) {
		if (slide.hasOwnProperty(x)) {
			slide_archive[slide.zoom][slide.stage][slide.section][x] = slide[x];
		}
	}

	readslide(w, h);
}

function readslide(w, h) {
	var slidewidth = w;
	var slideheight = h;

	$("#selected_bar").css("top", slide.bartop);

	$("#tissues").html(slide.tissues);

	if (slide.labelpic == '') $("#labelpic").css("display","none");
	else $("#labelpic").css("display","");

	$("#slideloc").html(slide.slideloc);
	$("#embryonum").html(slide.embryonum);
	$("#inputsection").val(slide.section);
	$("#inputstage").val(slide.stage);
	$("#selected_bar").css({"height":slide.barheight+"px", "top":slide.bartop+"px"});

	if (slide.nextzoom == slide.zoom) $("#in").attr("class","grayed");
	else $("#in").attr("class","");

	if (slide.prevzoom == slide.zoom) $("#out").attr("class","grayed");
	else $("#out").attr("class","");

	var oldoffset = $("#slpic").position();
	var offsetx = (slidewidth/2 - viewing_width/2 + oldoffset.left) / slidewidth * slide.width + viewing_width/2 - slide.width/2;
	var offsety = (slideheight/2 - viewing_height/2 + oldoffset.top) / slideheight * slide.height + viewing_height/2 - slide.height/2;
	if (!flytimer) $("#spinner").css("display","");
	$("#slidepic").attr({"src":slide.slidepic, "width":slide.width, "height":slide.height});
	$("#slpic").css({"width":slide.width+"px", "height":slide.height+"px", "left":offsetx+"px", "top":offsety+"px"});

	if (slide.zoom == 0) $("#labelbox").css("display","");
	else $("#labelbox").css("display","none");
	$("#labelpic").attr({"src":slide.labelpic, "width":slide.width, "height":slide.height});

	if (slide.keywords) {
		$("#keywords").html("Keywords: "+slide.keywords);
	} else {
		$("#keywords").html("");
	}

	$("#minimap").attr({"src":slide.minimap});
	$("#minimap2").html(slide.map);
	
	$(".navthumb a").each(function() {
		$(this).removeClass("selected");
	});
	$("#stage"+slide.stage).addClass("selected");
}
	
function updatetissue(key, value) {
	if (slide[key] == value) return false;
	slide[key] = value;
	var slidewidth = slide.width;
	var slideheight = slide.height;
	if (key == 'zoom') {
		$("#ruler").css("display","none");
		$("#rulernum").css("display","none");
	}
	$.ajax({url:'drem_tissue_json.php', data:{"id":slide.id,"zoom":slide.zoom}, success:function(data) {
		slide = jQuery.parseJSON(data);

		$("#slideloc").html(slide.slideloc);
		$("#inputsection").val(slide.id);

		if (slide.nextzoom == slide.zoom) $("#in").attr("class","grayed");
		else $("#in").attr("class","");

		if (slide.prevzoom == slide.zoom) $("#out").attr("class","grayed");
		else $("#out").attr("class","");

		var oldoffset = $("#slpic").position();
		var offsetx = (slidewidth/2 - viewing_width/2 + oldoffset.left) / slidewidth * slide.width + viewing_width/2 - slide.width/2;
		var offsety = (slideheight/2 - viewing_height/2 + oldoffset.top) / slideheight * slide.height + viewing_height/2 - slide.height/2;
		$("#spinner").css("display","");
		$("#slidepic").attr({"src":slide.slidepic, "width":slide.width, "height":slide.height});
		$("#slpic").css({"width":slide.width+"px", "height":slide.height+"px", "left":offsetx+"px", "top":offsety+"px"});

		$("#labelpic").attr({"src":slide.labelpic});
		$("#slidetitle").html(slide.title);
		$("#backslide").html(slide.backslide);

	}});
	return false;
}
		
function selectmode(m) {
	if (m == 'ruler') {
		map.viewingBox.style.cursor='crosshair';
		$("#ruler").css("display","none");
		$("#rulernum").css("display","none");
		$("#rulertool").addClass("selected");
		$("#movetool").removeClass("selected");
	} else {
		map.viewingBox.style.cursor=cU;
		$("#rulertool").removeClass("selected");
		$("#movetool").addClass("selected");
	}
	mode = m;
	return false;
}

function srClick(oEvent) {
	if ($(this).hasClass("searchnav")) return;
	if (oEvent.stopPropagation) oEvent.stopPropagation(); 
	srSelect(this);	
}

function srSelect(node) {
	$(node).focus();
	var array = $(node).html().split('-');
	if (array[2]) {
		array[0] = array[0]+'-'+array[1];
		array[1] = array[2];
	}

	$("#searchresult a").each(function(i, n) {
		$(n).removeClass("selected");
	});
	$(node).addClass("selected");

	labels = 1;
	$("#labelon").css("display", "");
	$("#labeloff").css("display", "none");
	$("#labelvis").css("display", "");

	slide.zoom = 0;
	updateslide('section', array[1], 'stage', array[0]);
}

function srNext() {
	var srFound = false;
	$("#searchresult a").each(function(i, n) {
		if ($(n).hasClass("searchnav")) {
			return true;
		}
		if (srFound) {
			srSelect(n);
			srFound = false;
			return false;
		}
		if ($(n).hasClass("selected")) {
			srFound = true;
		}
	});
	if (srFound) {
		$("#searchresult a").each(function(i, n) {
			if ($(n).hasClass("searchnav")) {
				return true;
			}
			srSelect(n);
			return false;
		});
	}
	return false;
}

function srPrev() {
	var prevNode = null;
	$("#searchresult a").each(function(i, n) {
		if ($(n).hasClass("searchnav")) {
			return true;
		}
		if ($(n).hasClass("selected") && prevNode) {
			srSelect(prevNode);
			prevNode = null;
			return false;
		}
		prevNode = n;
	});
	if (prevNode) srSelect(prevNode);
	return false;
}

function srMouseOver() {
	
}

function srMouseOut() {
	
}

var flytimer;
function startFlythrough() {
 	togglelabel(0);
	updateslide('zoom',0);
 	document.getElementById("playbutton").style.display = "none";
	document.getElementById("pausebutton").style.display = "";
	flythrough();
	return false;
}

function stopFlythrough() {
	window.clearTimeout(flytimer);
	flytimer = null;
	document.getElementById("playbutton").style.display = "";
	document.getElementById("pausebutton").style.display = "none";
	return false;
}

function flythrough() {
	updateslide('section',slide.nextsection);
	flytimer = window.setTimeout(flythrough, 1000*Math.pow(2, -document.getElementById("flyspeed").value));
	return false;
}
