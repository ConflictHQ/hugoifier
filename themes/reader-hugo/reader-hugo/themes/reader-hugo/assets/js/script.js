// other script
(function () {
	'use strict';

	// -----------------------------------------------
	// Header fixed
	window.addEventListener('scroll', function () {
		var scrolling = window.pageYOffset;
		var navigation = document.querySelector('.navigation');
		if (scrolling > 10) {
			navigation.classList.add('nav-bg');
		} else {
			navigation.classList.remove('nav-bg');
		}
	});


	// -----------------------------------------------
	// Post slider swiper js
	new Swiper('.post-slider.swiper', {
		slidesPerView: 1,
		spaceBetween: 30,
		loop: true,
		autoplay: {
			delay: 2500,
			disableOnInteraction: false,
		},
		navigation: {
			nextEl: '.post-slider .swiper-button-next',
			prevEl: '.post-slider .swiper-button-prev',
		},
	});

	// -----------------------------------------------
	// Instafeed
	let instafeed = document.querySelectorAll('#instafeed');
	if ((instafeed.length) !== 0) {
		var accessToken = instafeed.getAttribute('data-accessToken');
		var userFeed = new Instafeed({
			get: 'user',
			resolution: 'low_resolution',
			accessToken: accessToken,
			template: '<div class="instagram-post"><a href="{{link}}" target="_blank"><img src="{{image}}"></a></div>'
		});
		userFeed.run();
	}

	setTimeout(function () {
		let instagramSlider = document.querySelector(".instagram-slider");
		instagramSlider.classList.add('show');

		new Swiper('.instagram-slider', {
			spaceBetween: 10,
			loop: true,
			grabCursor: true,
			autoplay: {
				delay: 2500,
			},
			breakpoints: {
				// when window width is >= 480px
				0: {
					slidesPerView: 2,
				},
				// when window width is >= 600px
				600: {
					slidesPerView: 4,
				},
				// when window width is >= 1024px
				1024: {
					slidesPerView: 8,
				},
			}
		});

	}, 1000);

	// -----------------------------------------------
	// Popup video
	let videoSrc;
	let videoModal = document.getElementById('videoModal');
	if (videoModal) {
		document.querySelectorAll('.video-btn').forEach(function (btn) {
			btn.addEventListener('click', function () {
				videoSrc = this.getAttribute('data-src');
			});
		});

		videoModal?.addEventListener('shown.bs.modal', function () {
			document.querySelector('#videoModal iframe').setAttribute('src', videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
		});

		videoModal?.addEventListener('hide.bs.modal', function () {
			document.querySelector('#videoModal iframe').setAttribute('src', '');
		});
	}

	// gallery slider
	new Swiper(".gallery-slider", {
		slidesPerView: 1,
		loop: true,
		autoHeight: true,
		spaceBetween: 0,
		speed: 1500,
		autoplay: {
			delay: 5000,
		},
		navigation: {
			nextEl: ".swiper-button-next",
			prevEl: ".swiper-button-prev",
		},
	});

})();