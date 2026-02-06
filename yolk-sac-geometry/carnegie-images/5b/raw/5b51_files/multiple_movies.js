var currentPlayer=null;
var currentFile;
var currentImage;
var currentLanguage;

function createPlayer (thePlace, theFile, theImage, go, theLanguage, forceCaptions) {
	if (currentPlayer!=null) { jwplayer(currentPlayer).remove() }
	currentPlayer=thePlace;
	currentFile=theFile;
	currentImage=theImage;
	currentLanguage=theLanguage;

	var captionfile, captionstate;
	if (forceCaptions || (theLanguage && theLanguage != 25)) {
		captionfile = 'http://'+location.host+'/movie-caption.srt.php?param=0+'+theLanguage+"+"+theFile;
		captionstate = 'true';
	} else {
		captionfile = 'http://'+location.host+'/movie-caption.srt.php?param=0+0+'+theFile;
		captionstate = 'false';
	}
	
	jwplayer(thePlace).setup({
		flashplayer: "/flash/controls/player5.9.swf",
		skin: "/flash/skins/classic/classic.zip",
		"controlbar.position": "bottom",
		file: theFile,
		image: theImage,
		width: 320,
		height: 259,
		plugins: "/flash/plugins/captions.js,/flash/plugins/yourlytics.js",
		"captions.file": captionfile,
		"captions.fontWeight": "bold",
		"captions.color": "#FFFF00",
		"captions.fontSize": 16,
		"captions.state": captionstate,
		"yourlytics.callback": "/movie_log.php?w=ehd.org",
		"dock": "false",
		autostart: (go ? true : false)
	});
	return false;
}
