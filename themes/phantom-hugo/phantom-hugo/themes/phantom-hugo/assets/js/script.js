(function ($) {
	"use strict";

	$(window).on("load", function () {
		$(".preloader").addClass("active");
		isotopeMasonry();
		setTimeout(function () {
			$(".preloader").addClass("done");
		}, 1500);
	});

	$(".history-scroller").niceScroll({
		cursorwidth: "10px",
		background: "#0d1015",
		cursorborder: "0",
		cursorborderradius: "0",
		autohidemode: false,
		zindex: 5
	});

	$(".testimonials").owlCarousel({
		margin: 30,
		autoPlay: true,
		autoPlay: 5000,
		responsive: {
			0: {
				items: 1
			},
			480: {
				items: 1
			},
			768: {
				items: 1
			},
			1024: {
				items: 2
			}
		}
	});

	animatedProgressBar();
	windowHieght();

	function animatedProgressBar() {
		$(".progress").each(function () {
			var skillValue = $(this).find(".skill-lavel").attr("data-skill-value");
			$(this).find(".bar").animate({
				width: skillValue
			}, 1500, "easeInOutExpo");

			$(this).find(".skill-lavel").text(skillValue);
		});
	}

	function windowHieght() {
		if ($(window).height() <= 768) {
			$(".pt-table").addClass("desktop-768");
		} else {
			$(".pt-table").removeClass("desktop-768");
		}
	}

	/*----------------------------------------
		Isotope Masonry
	------------------------------------------*/
	function isotopeMasonry() {
		$(".isotope-gutter").isotope({
			itemSelector: '[class^="col-"]',
			percentPosition: true
		});
		$(".isotope-no-gutter").isotope({
			itemSelector: '[class^="col-"]',
			percentPosition: true,
			masonry: {
				columnWidth: 1
			}
		});

		$(".filter a").on("click", function () {
			$(".filter a").removeClass("active");
			$(this).addClass("active");
			// portfolio fiter
			var selector = $(this).attr("data-filter");
			$(".isotope-gutter").isotope({
				filter: selector,
				animationOptions: {
					duration: 750,
					easing: "linear",
					queue: false
				}
			});
			return false;
		});
	}

})(jQuery);