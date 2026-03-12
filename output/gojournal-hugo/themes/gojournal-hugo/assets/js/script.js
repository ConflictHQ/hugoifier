// Preloader js    
$(window).on('load', function () {
	$('.preloader').fadeOut(100);
});
(function ($) {
	'use strict';

	//  Search Form Open
	$('#searchOpen').on('click', function () {
		$('.search-collapsed').addClass('open');
		setTimeout(function () {
			$('.search-collapsed input').focus();
		}, 400);
	});
	$('#searchClose').on('click', function () {
		$('.search-collapsed').removeClass('open');
	});

	// featured post slider
	$('.post-slider').slick({
		infinite: true,
		slidesToShow: 1,
		slidesToScroll: 1,
		arrows: false,
		dots: true
	});


	// instafeed
	if (($('#instafeed').length) !== 0) {
		var userId = $('#instafeed').attr('data-userId');
		var accessToken = $('#instafeed').attr('data-accessToken');
		var userFeed = new Instafeed({
			get: 'user',
			userId: userId,
			limit: 6,
			resolution: 'thumbnail',
			accessToken: accessToken,
			// for more options, visit http://instafeedjs.com/
			template: '<div class="col-4 px-1 mb-2"><a href="{{link}}" target="_blank"><img class="img-fluid w-100" src="{{image}}" alt="instagram-image"></a></div>'
		});
		userFeed.run();
	}



	// tab
	$('.tab-content').find('.tab-pane').each(function (idx, item) {
		var navTabs = $(this).closest('.code-tabs').find('.nav-tabs'),
			title = $(this).attr('title');
		navTabs.append('<li class="nav-item"><a class="nav-link" href="#">' + title + '</a></li>');
	});

	$('.code-tabs ul.nav-tabs').each(function () {
		$(this).find("li:first").addClass('active');
	})

	$('.code-tabs .tab-content').each(function () {
		$(this).find("div:first").addClass('active');
	});

	$('.nav-tabs a').click(function (e) {
		e.preventDefault();
		var tab = $(this).parent(),
			tabIndex = tab.index(),
			tabPanel = $(this).closest('.code-tabs'),
			tabPane = tabPanel.find('.tab-pane').eq(tabIndex);
		tabPanel.find('.active').removeClass('active');
		tab.addClass('active');
		tabPane.addClass('active');
	});

	// Accordions
	$('.collapse').on('shown.bs.collapse', function () {
		$(this).parent().find('.ti-plus').removeClass('ti-plus').addClass('ti-minus');
	}).on('hidden.bs.collapse', function () {
		$(this).parent().find('.ti-minus').removeClass('ti-minus').addClass('ti-plus');
	});

})(jQuery);