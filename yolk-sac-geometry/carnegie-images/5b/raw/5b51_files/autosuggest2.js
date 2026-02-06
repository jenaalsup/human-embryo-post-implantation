/**
 * Autosuggests one or more suggestions for what the user has typed.
 * If no suggestions are passed in, then no autosuggest occurs.
 * @scope private
 * @param aSuggestions An array of suggestion strings.
 * @param bTypeAhead If the control should provide a type ahead suggestion.
 */
function autosuggest(aSuggestions /*:Array*/) {
    //make sure there's at least one suggestion
    if (aSuggestions && aSuggestions.length > 0) {
        showSuggestions(aSuggestions);
    } else {
        hideSuggestions();
    }
};

var cur = -1;
var currentTB;

var dropdown = document.createElement("div");
dropdown.className = "suggestions";
dropdown.style.visibility = "hidden";
dropdown.style.width = "200px";
    
dropdown.onmousedown = 
dropdown.onmouseup = 
dropdown.onmouseover = function (oEvent) {
	oEvent = oEvent || window.event;
	oTarget = oEvent.target || oEvent.srcElement;

	if (oEvent.type == "mousedown") {
		currentTB.value = oTarget.firstChild.nodeValue;
		hideSuggestions();
	} else if (oEvent.type == "mouseover") {
		highlightSuggestion(oTarget);
	} else {
		currentTB.focus();
	}
};

function hideSuggestions() {
	dropdown.style.visibility = "hidden";
}

/**
 * Highlights the given node in the suggestions dropdown.
 * @scope private
 * @param oSuggestionNode The node representing a suggestion in the dropdown.
 */
function highlightSuggestion(oSuggestionNode) {
    
	if (!dropdown.childNodes) return;
    for (var i=0; i < dropdown.childNodes.length; i++) {
        var oNode = dropdown.childNodes[i];
        if (oNode == oSuggestionNode) {
            oNode.className = "current"
        } else if (oNode.className == "current") {
            oNode.className = "";
        }
    }
};

function handleFocus(oEvent) {
	currentTB = oEvent.target;
	$(this).select();	
}

function handleBlur(oEvent) {
	hideSuggestions();
	if (typeof submitData == 'function') submitData(this);
	currentTB = null;
}

function handleKeydown (oEvent) {
    switch(oEvent.keyCode) {
        case 38: //up arrow
            previousSuggestion();
            break;
        case 40: //down arrow 
            nextSuggestion();
            break;
        case 13: //enter
            hideSuggestions();
            oEvent.preventDefault();
            oEvent.stopPropagation();
            break;
    }
}

function handleKeyup (oEvent) {
    var iKeyCode = oEvent.keyCode;

    //for backspace (8) and delete (46), shows suggestions without typeahead
    if (iKeyCode == 8 || iKeyCode == 46) {
		requestSuggestions();
        
    //make sure not to interfere with non-character keys
    } else if (iKeyCode < 32 || (iKeyCode >= 33 && iKeyCode < 46) || (iKeyCode >= 112 && iKeyCode <= 123)) {
        //ignore
    } else {
        //request suggestions from the suggestion provider with typeahead
		requestSuggestions();
    }
}

/**
 * Highlights the next suggestion in the dropdown and
 * places the suggestion into the textbox.
 * @scope private
 */
function nextSuggestion() {
    var cSuggestionNodes = dropdown.childNodes;

	//if (this.cur == cSuggestionNodes.length-1) this.cur = 0;
    if (cSuggestionNodes.length > 0 && cur < cSuggestionNodes.length-1) {
        var oNode = cSuggestionNodes[++cur];
		highlightSuggestion(oNode);
		currentTB.value = oNode.firstChild.nodeValue; 
    }
};

/**
 * Highlights the previous suggestion in the dropdown and
 * places the suggestion into the textbox.
 * @scope private
 */
function previousSuggestion() {
    var cSuggestionNodes = dropdown.childNodes;

	//if (this.cur == 0) this.cur = cSuggestionNodes.length-1;
    if (cSuggestionNodes.length > 0 && cur > 0) {
        var oNode = cSuggestionNodes[--cur];
		highlightSuggestion(oNode);
        currentTB.value = oNode.firstChild.nodeValue;   
    }
};

function showSuggestions(aSuggestions /*:Array*/) {
	if (currentTB == null) return;
	
	cur = -1;
    var oDiv = null;
	dropdown.innerHTML = "";  //clear contents of the layer
    
    for (var i=0; i < aSuggestions.length; i++) {
        oDiv = document.createElement("div");
        oDiv.appendChild(document.createTextNode(aSuggestions[i]));
        dropdown.appendChild(oDiv);
    }
	dropdown.style.left = $(currentTB).offset().left + "px";
	dropdown.style.top = $(currentTB).offset().top + $(currentTB).outerHeight() + "px";
	dropdown.style.width = $(currentTB).width() + "px";
	dropdown.style.visibility = "visible";
};

