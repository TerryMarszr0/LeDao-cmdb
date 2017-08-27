
function initGrid(options) {
	
	var toolBar = options.toolBar;
	var pageBar = options.pageBar;
	if(typeof toolBar == 'undefined') toolBar = "myInput";
	if(typeof pageBar == 'undefined') pageBar = "footPage";
	var myInput = $("#" + toolBar);
	var toolHtml = myInput.html();
	var page = $("#" + pageBar);
	var pageHtml = page.html();

	page.remove();
	myInput.remove();
	
	var _options = {
		renderTo: "",
	    ajax: true,
	    post: function () {
	    
			var params = {};
			
	    	/**获取所有class为my-form的表单中的元素名和值*/
	    	var form = $(".my-form");
	    	if(typeof form != 'undefined') {
		    	var arr = form.serializeArray();
		    	$.each(arr, function(i, field){
			   		params[field.name] = field.value;
			  	});
	    	}
	        return params;
	    },
	    url: '',
	    head: [],
	    selection: true,
	    multiSelect: true,
	    rowCount: [25, 100, 500, 1000],
	    formatters: {
	        "commands": function(column, row) {
		    	var rowID = row["commands"];
		    	if(typeof rowID == 'undefined') {
					for(var i in row) {
						rowID = row[i];
						break;
					}
		        }
		        return "<button type=\"button\" class=\"btn btn-xs btn-default command-edit\" data-row-id=\"" + rowID + "\" title='编辑'><span class=\"glyphicon glyphicon-edit\" ></span></button>　" + 
		            "<button type=\"button\" class=\"btn btn-xs btn-default command-delete\" data-row-id=\"" + rowID + "\"  title='删除'><span class=\"glyphicon glyphicon-ban-circle\" ></span></button>";
	        }
	    },
	    templates: {
	    	footer: "<div id=\"{{ctx.id}}\" class=\"{{css.footer}}\"><div class=\"row\">" 
		    	+ pageHtml 
		    	+ "</div></div>",
	        header: "<div id=\"{{ctx.id}}\" class=\"{{css.header}} dan-table-menu form form-inline\">" 
				+ toolHtml
	            + "</div>",
		}
	}
	
	var myOptions = $.extend({}, _options, options);
	var divID = myOptions.renderTo;
	var head = myOptions.head;
	var myThead = $('<table id="my_bootgrid" class="table table-condensed table-hover table-striped"><thead><tr id="my_grid_tr"></tr></thead></table>').appendTo("#" + divID);	
	$.each(head, function(i, v) {
		var th = '<th data-column-id="' + v.key + '" id="' + v.key + '"';
		if(v.identifier) {
			th += ' data-identifier="true" ';
		}
		th += '>' + v.text + '</th>';
		$("#my_grid_tr").append(th);
	});
	var grid = $("#my_bootgrid").bootgrid(myOptions);
	var thArr = $("#my_bootgrid").find("thead tr th");
	
	var i = 0;
	thArr.each(function() {
		var h = head[i];
		if(typeof h.cls != "undefined") {
			$(this).css(h.cls);
		}
		i++;
	});
	return grid;
}