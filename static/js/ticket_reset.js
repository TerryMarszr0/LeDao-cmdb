// JavaScript Document

//start鼠标滑过展开菜单
$(document).ready(function(){

	/**
	 * 鼠标划过就展开子菜单，免得需要点击才能展开
	 */ 
	function dropdownOpen() {
	
		var $dropdownLi = $('li.dropdown');
	
		$dropdownLi.mouseover(function() {
			$(this).addClass('open');
		}).mouseout(function() {
			$(this).removeClass('open');
		});
	}
	
	//置顶按钮的js当鼠标滚动才出现
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
	});
	//置顶按钮的js--end
	
	//收藏按钮，空心变实心
	/*
	$("#loveicon").click(function(){
	 $("#loveicon i").addClass("glyphicon-heart");//增加class
	 $("#loveicon i").removeClass("glyphicon-heart-empty");//移除class
	});
	*/
	//右侧菜单的触发	
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
































