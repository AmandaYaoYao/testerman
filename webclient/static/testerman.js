/**
 * Several basic functions to add some features
 * in ATS log views.
 */

function expandCollapse(id) {
  var element = document.getElementById(id);
  element.style.display = (element.style.display != "block" ? "block" : "none"); 
}

/* expand/collapse all div elements whose id starts with s */
function expandCollapseAll(s) {
  var elements = document.getElementsByTagName("div");
  for (var i = 0; i < elements.length; i++) {
    if (elements[i].id.substring(0, s.length) == s) {
			elements[i].style.display = (elements[i].style.display != "block" ? "block" : "none");	
		}
	}
}


function htmlEscape(s) {
	var e = document.createElement("div");
	e.innerText = e.textContent = s;
	return e.innerHTML;
}

// Get the text content of an element - all browsers
function getText(element) {
	if (element.textContent) {
		return element.textContent;
	} else {
		return element.innerText; // IE specific
	}
}

function base64DecodeById(id, replaceCR) {
	var element = document.getElementById(id);
	var decoded = Base64.decode(getText(element))
	
	if (replaceCR) {
		// replace \n by br
		decoded = htmlEscape(decoded);
		decoded = decoded.replace(/\n/g, '<br />');
		element.innerHTML = decoded;
	}
	else {
		// innerText for IE, textContent for anything else
		element.innerText = element.textContent = decoded;
	}
}


// Base 64 encoder, from http://www.webtoolkit.info/
var Base64 = {
	// private property
	_keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
 
	// public method for decoding
	decode : function (input) {
		var output = "";
		var chr1, chr2, chr3;
		var enc1, enc2, enc3, enc4;
		var i = 0;
		input = input.replace(/[^A-Za-z0-9\+\/\=]/g, ""); 
		while (i < input.length) {
 			enc1 = this._keyStr.indexOf(input.charAt(i++));
			enc2 = this._keyStr.indexOf(input.charAt(i++));
			enc3 = this._keyStr.indexOf(input.charAt(i++));
			enc4 = this._keyStr.indexOf(input.charAt(i++)); 
			chr1 = (enc1 << 2) | (enc2 >> 4);
			chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
			chr3 = ((enc3 & 3) << 6) | enc4; 
			output = output + String.fromCharCode(chr1); 
			if (enc3 != 64) {
				output = output + String.fromCharCode(chr2);
			}
			if (enc4 != 64) {
				output = output + String.fromCharCode(chr3);
			} 
		}
		output = Base64._utf8_decode(output); 
		return output;
	},
 
	// private method for UTF-8 decoding
	_utf8_decode : function (utftext) {
		var string = "";
		var i = 0;
		var c = c1 = c2 = 0;
 
		while ( i < utftext.length ) {
 
			c = utftext.charCodeAt(i);
 
			if (c < 128) {
				string += String.fromCharCode(c);
				i++;
			}
			else if((c > 191) && (c < 224)) {
				c2 = utftext.charCodeAt(i+1);
				string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
				i += 2;
			}
			else {
				c2 = utftext.charCodeAt(i+1);
				c3 = utftext.charCodeAt(i+2);
				string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
				i += 3;
			}
		}
		return string;
	}
}