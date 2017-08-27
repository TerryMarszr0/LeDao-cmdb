// JavaScript Document

//start鼠标滑过展开菜单
$(document).ready(function(){
	
	/**下拉菜单导航条不可点击的问题
	 *$(document).off('click.bs.dropdown.data-api');
	 */
	$(document).on("click",".dropdown-toggle",function(){
    if($(this).attr('href')) window.location = $(this).attr('href');
     });
	/**
	 * 鼠标划过就展开子菜单，免得需要点击才能展开
	 */ 
	dropdownOpen();//调用
	function dropdownOpen() {
	
		var $dropdownLi = $('li.dropdown');
	
		$dropdownLi.mouseover(function() {
			$(this).addClass('open');
		}).mouseout(function() {
			$(this).removeClass('open');
		});
	  }

	/**
	  *解决样式抖动问题
	 */	
        function reLoad() {
            var docH = $(document).height(); //文档高度
            var wH = $(window).height(); //窗口可视高度
            if (docH > wH) {
				//执行内容
				  //由于bootstrap框架控制，当文档内容大于窗口可视高度出现抖动           
				  $('.modal').on('show.bs.modal', function (event) {
					  $('.mod-scroll-btn').css({
						  'margin-right': '17px'
					  })
					  $('.top-bar').css({
						  'padding-right': '17px'
					  })
					  $('.navbar').css({
						  'padding-right': '17px'
					  })
					  });
					  
				  $('.modal').on('hidden.bs.modal', function (event) {
					  $('.mod-scroll-btn').css({
						  'margin-right': '0px'
					  })
					  $('.top-bar').css({
						  'padding-right': '0px'
					  })
					  $('.navbar').css({
						  'padding-right': '0px'
					  })
					  });
				//执行内容end
            } 
        }
        $(function () {
            reLoad();
        });
        $(window).resize(function () {
            reLoad();
        });
	
	
	/**
	 *置顶按钮的js当鼠标滚动才出现
	 */
	$("#back-to-top").hide();
	$(function () {
		$(window).scroll(function(){
		if ($(window).scrollTop()>50){
		$("#back-to-top").fadeIn(500);
	}
	else
	{
	$("#back-to-top").fadeOut(500);
	}
	});
	$("#back-to-top").click(function(){
	$('body,html').animate({scrollTop:0},100);
	return false;
	});
	});//置顶按钮的js--end
	
	/*收藏按钮，空心变实心
	* $("#loveicon").click(function(){
	  $("#loveicon i").addClass("glyphicon-heart");//增加class
	  $("#loveicon i").removeClass("glyphicon-heart-empty");//移除class
	});
    */
	
	/*
	*右侧菜单的触发
	*/	
	$("#mod-scroll").mouseover(function(){
		$("#scoll-dropdown").show();
		$(".hide-show p").hide();
		$("#toggle-menu i").addClass("glyphicon-chevron-up");//增加class
	    $("#toggle-menu i").removeClass("glyphicon-chevron-down");//移除class
	});
	$("#mod-scroll").mouseout(function(){
		$("#scoll-dropdown").hide();
		$(".hide-show p").show();
		$("#toggle-menu i").addClass("glyphicon-chevron-down");//增加class
	    $("#toggle-menu i").removeClass("glyphicon-chevron-up");//移除class
	});

	
	
	
});
































