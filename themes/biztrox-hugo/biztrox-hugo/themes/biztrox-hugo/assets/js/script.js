(function () {
	'use strict';

	// Element Existence Checker Function
	function isElementExist(element) {
		if (element) {
			return true;
		}
		return false;
	}

	// ----------------------------
	// Sliders
	// ---------------------------- 

	// Hero Slider
	new Swiper('.hero-slider', {
		slidesPerView: 1,
		loop: true,
		centeredSlides: true,
		autoplay: {
			delay: 10000,
		},
		navigation: {
			nextEl: '.swiper-navigation .nextArrow',
			prevEl: '.swiper-navigation .prevArrow',
		},
		pagination: {
			el: '.hero-slider .swiper-pagination',
			clickable: true,
			renderBullet: function (index, className) {
				let icon = document.querySelectorAll('.hero-slider .swiper-slide')[index + 1].getAttribute('data-icon');
				let text = document.querySelectorAll('.hero-slider .swiper-slide')[index + 1].getAttribute('data-text');
				return '<li class="' + className + '"><a href="#?"><i class="' + icon + '"></i><span>' + text + '</span></a></li>';
			},
		},
	});

	// Work Slider
	new Swiper('.work-slider', {
		slidesPerView: 4,
		loop: true,
		slidesPerGroup: 4,
		autoplay: {
			delay: 10000,
		},
		pagination: {
			el: '.work-slider+.swiper-pagination',
			clickable: true,
		},
		breakpoints: {
			0: {
				slidesPerView: 1,
				slidesPerGroup: 1,
			},
			576: {
				slidesPerView: 2,
				slidesPerGroup: 2,
			},
			768: {
				slidesPerView: 3,
				slidesPerGroup: 3,
			},
			991: {
				slidesPerView: 4,
				slidesPerGroup: 4,
			},
		}
	});

	// testimonial slider
	new Swiper('.testimonial-slider', {
		slidesPerView: 1,
		centeredSlides: true,
		spacebetween: 80,
		autoplay: {
			delay: 2000,
		},
		navigation: {
			prevEl: '.swiper-navigation .prevArrow',
			nextEl: '.swiper-navigation .nextArrow',
		},
	});

	// Client Logo Slider
	new Swiper('.client-logo-slider', {
		loop: true,
		autoplay: {
			delay: 2400,
		},
		breakpoints: {
			0: {
				slidesPerView: 2,
			},
			576: {
				slidesPerView: 3,
			},
			1024: {
				slidesPerView: 5,
			},
		}
	});

	// back to top button in plain js
	let backToTop = document.querySelector('.back-to-top');
	backToTop.addEventListener('click', function () {
		document.body.scrollTop = 0;
		document.documentElement.scrollTop = 0;
	});

	// -----------------------------
	//  Video Replace
	// ----------------------------- 

	let videoPlayBtn = document.querySelector(".promo-video .play-icon");
	let videoModal = document.querySelector("#videoModal");

	if (isElementExist(videoPlayBtn)) {
		videoPlayBtn.addEventListener("click", function () {
			let videoIframe = document.querySelector("#videoModal iframe");
			let videoLink = videoPlayBtn.getAttribute("video-url");
			videoIframe.setAttribute("src", videoLink);
		});

		videoModal.addEventListener("hidden.bs.modal", function () {
			let videoIframe = document.querySelector("#videoModal iframe");
			videoIframe.setAttribute("src", "");
		});
	};

	document.addEventListener("DOMContentLoaded", function () {

		// ----------------------------
		// Filter
		// ---------------------------- 

		let filterContainer = document.querySelector('.filter-container');
		if (isElementExist(filterContainer)) {
			new Filterizr('.filter-container')
		}

		// active changer
		let control = document.querySelectorAll('.control');
		control.forEach(function (item) {
			item.addEventListener('click', function () {
				control.forEach(function (item) {
					item.classList.remove('active');
				});
				this.classList.add('active');
			});
		});

		// ----------------------------
		// Counter
		// ---------------------------- 

		// You can change this class to specify which elements are going to behave as counters.
		let elements = document.querySelectorAll(".counter");

		elements.forEach(function (item) {
			// Add new attributes to the elements with the '.counter' HTML class
			item.counterAlreadyFired = false;
			item.counterSpeed = item.getAttribute("data-counter-time") / 45;
			item.counterTarget = +item.innerText;
			item.counterCount = 0;
			item.counterStep = item.counterTarget / item.counterSpeed;

			item.updateCounter = function () {
				item.counterCount = item.counterCount + item.counterStep;
				item.innerText = Math.ceil(item.counterCount);

				if (item.counterCount < item.counterTarget) {
					setTimeout(item.updateCounter, item.counterSpeed);
				} else {
					item.innerText = item.counterTarget;
				}
			};
		});

		// Function to determine if an element is visible in the web page
		let isElementVisible = function isElementVisible(el) {
			let scroll = window.scrollY || window.pageYOffset;
			let boundsTop = el.getBoundingClientRect().top + scroll;
			let viewport = {
				top: scroll,
				bottom: scroll + window.innerHeight,
			};
			let bounds = {
				top: boundsTop,
				bottom: boundsTop + el.clientHeight,
			};
			return (
				(bounds.bottom >= viewport.top && bounds.bottom <= viewport.bottom) ||
				(bounds.top <= viewport.bottom && bounds.top >= viewport.top)
			);
		};

		// Funciton that will get fired uppon scrolling
		let handleScroll = function handleScroll() {
			elements.forEach(function (item, id) {
				if (true === item.counterAlreadyFired) return;
				if (!isElementVisible(item)) return;
				item.updateCounter();
				item.counterAlreadyFired = true;
			});
		};

		// Fire the function on scroll
		window.addEventListener("scroll", handleScroll);
	});
})();