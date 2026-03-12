// Preloader js    
$(window).on('load', function () {
	$('.preloader').fadeOut(100);
});

(function ($) {
	'use strict';

	$('#dn').on('change', function () {
		if ($(this).prop('checked') == false) {
			$('body').addClass('light');
			localStorage.setItem('light', this.checked);
		} else {
			$('body').removeClass('light');
			localStorage.removeItem('light');
		}
	});

	if (localStorage.getItem('light')) {
		$('body').addClass('light');
		$("#dn").prop("checked", false);
	} else {
		$("#dn").prop("checked", true);
	}

})(jQuery);