function getParams() { 
	var params = {};
	var url = location.href; 
	var start = url.indexOf("?") + 1;
	if (start == 0)
		return params;	
	var end = url.indexOf("#") == -1?url.length : url.indexOf("#");
	var queryString = url.substring(start, end);
	var paraString = queryString.split('&');
	var cur = "";
	for (var i=0; i < paraString.length; i++) { 
		cur = paraString[i];
		var pos = cur.indexOf("=");
		params[cur.substring(0, pos)] = urlDecode(cur.substring(pos + 1, cur.length)); 
	}
	return params;
}

function getUrl() { 
	var url = location.href; 
	var end = url.indexOf("?");
	if (end == 0) return url;	
	return url.substring(0, end);
}

function getUrlParams(url) { 
	var params = {};
	var start = url.indexOf("?") + 1;
	if (start == 0)
		return params;	
	var end = url.indexOf("#") == -1?url.length : url.indexOf("#");
	var queryString = url.substring(start, end);
	var paraString = queryString.split('&');
	var cur = "";
	for (var i=0; i < paraString.length; i++) { 
		cur = paraString[i];
		var pos = cur.indexOf("=");
		params[cur.substring(0, pos)] = urlDecode(cur.substring(pos + 1, cur.length)); 
	}
	return params;
}

function getUrlPath(url) { 
	var end = url.indexOf("?");
	if (end == 0) return url;	
	return url.substring(0, end);
}

Date.prototype.format = function(format){

	var o = { 
		"M+" : this.getMonth() + 1, //month 
		"d+" : this.getDate(), //day 
		"h+" : this.getHours(), //hour 
		"m+" : this.getMinutes(), //minute 
		"s+" : this.getSeconds(), //second 
		"q+" : Math.floor((this.getMonth() + 3)/3), //quarter 
		"S" : this.getMilliseconds() //millisecond 
	} 
	
	if(/(y+)/.test(format)) { 
		format = format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length)); 
	} 
	
	for(var k in o) { 
		if(new RegExp("("+ k +")").test(format)) { 
			format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length)); 
		} 
	} 
	return format; 
}

function urlDecode(zipStr){  
    var uzipStr = "";  
    for(var i = 0; i < zipStr.length; i++){  
        var chr = zipStr.charAt(i);  
        if(chr == "+"){  
            uzipStr += " ";  
        }else if(chr == "%"){  
            var asc = zipStr.substring(i+1, i+3);  
            if(parseInt("0x" + asc)>0x7f){  
                uzipStr += decodeURI("%" + asc.toString() + zipStr.substring(i + 3, i + 9).toString());  
                i += 8;  
            }else{  
                uzipStr += AsciiToString(parseInt("0x" + asc));  
                i += 2;  
            }  
        }else{  
            uzipStr += chr;  
        }  
    }  
    return uzipStr;  
}  
  
function StringToAscii(str){  
    return str.charCodeAt(0).toString(16);  
}  
function AsciiToString(asccode){  
    return String.fromCharCode(asccode);  
}

function getQueryString() { 
	var params = {};
	var url = location.href; 
	var start = url.indexOf("?") + 1;
	if (start == 0)
		return '';	
	var end = url.indexOf("#") == -1?url.length:url.indexOf("#");
	var queryString = url.substring(start, end); 
	return queryString;
}

var by = function(name, order){
    return function(o, p){
        var a, b;
        if (typeof o === "object" && typeof p === "object" && o && p) {
            a = o[name];
            b = p[name];
            if (a === b) {
                return 0;
            }
            if (typeof a === typeof b) {
				if (order == 'DESC' || order == 'desc') {
					return a < b ? 1 : -1;
				} else {
					return a < b ? -1 : 1;
				}
            }
			if (order == 'DESC' || order == 'desc') {
				return typeof a < typeof b ? 1 : -1;
			} else {
				return typeof a < typeof b ? -1 : 1;
			}
        }
        else {
            throw ("error");
        }
    }
}

function trim(value) {
    return value.replace(/(^\s*)|(\s*$)/g, "");
}
