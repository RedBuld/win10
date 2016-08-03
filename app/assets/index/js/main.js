$(document).ready(function(){
	time();date();
	setInterval(time,500);
	setInterval(time,500);
	$('#menu').on('click',function(){
		if($('#menu').hasClass('open'))
		{
			$('#menu').removeClass('open');
			$('#menu_drawer').addClass('fadeOutDown').removeClass('fadeInUpLittle active');
		}else{
			$('#menu').addClass('open');
			$('#menu_drawer').removeClass('fadeOutDown').addClass('fadeInUpLittle active');
			$('#display').prepend('<div id="open_menu_trigger"></div>');
			$('#open_menu_trigger').on('click',function(){
				$('#menu').removeClass('open');
				$('#menu_drawer').addClass('fadeOutDown').removeClass('fadeInUpLittle active');
				$('#open_menu_trigger').off();
				$('#open_menu_trigger').remove();
			})
		}
	})
	new WOW({ mobile: false }).init();
	menu_scroller = baron({
        root: '.baron',
        scroller: '.baron__scroller',
        bar: '.baron__bar',
        scrollingCls: '_scrolling',
        draggingCls: '_dragging',
        impact: 'scroller',
    });
})
time = function(){
	var clck = new Date();
	var hrs = clck.getHours();
	var min = clck.getMinutes();
	if(min<10)
		min = "0"+min;
	$('#clock').html(hrs+':'+min);
}
date = function()
{
	var date = new Date();
	var day = date.getDate();
	var month = date.getMonth()+1;
	var year = date.getFullYear();
	if(day<10)
		day = "0"+day;
	if(month<10)
		month = "0"+month;
	$('#date').html(day+'.'+month+'.'+year);
}