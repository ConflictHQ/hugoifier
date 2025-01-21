(function ($) {
	'use strict';

	// prelaoder
	$('.preloader').delay(100).fadeOut(10);
	
	// sidenav-menu
	function sidenav() {
		$('[data-toggle="sidenav-menu"]').on('click', function () {
			$('.sidenav-menu, .sidenav-overlay').toggleClass('show');
		});
	}
	sidenav();

	// search-popup
	function searchPopup() {
		$('[data-toggle="search"]').on('click', function () {
			$('.search-block').fadeIn(200);
			setTimeout(function () {
				$('.search-block').addClass('is-visible');
				var value = $('#search-field').val();
				$('#search-field').focus().val('').val(value);
			}, 250);
		});
		$('[data-toggle="search-close"]').on('click', function () {
			$('.search-block').fadeOut(200).removeClass('is-visible');
		});
	}
	searchPopup();

	// menuHumBurger icon toggle Init
	function menuHumBurgerIcon() {
		$('.navbar-toggler').on('click', function () {
			$('i').toggleClass('d-inline d-none');
		});
	}
	menuHumBurgerIcon();


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
		$(this).parent().find('.fas fa-plus').removeClass('fas fa-plus').addClass('fas fa-minus');
	}).on('hidden.bs.collapse', function () {
		$(this).parent().find('.fas fa-minus').removeClass('fas fa-minus').addClass('fas fa-plus');
	});


	//post slider
	$('.post-slider').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		autoplay: true,
		autoplaySpeed: 1500,
		fade: true,
  	cssEase: 'linear',
		dots: false,
		arrows: true,
		prevArrow: '<button type=\'button\' class=\'prevArrow\'><i class=\'fas fa-angle-left\'></i></button>',
		nextArrow: '<button type=\'button\' class=\'nextArrow\'><i class=\'fas fa-angle-right\'></i></button>'
	});
	

})(jQuery);