// main script
(function () {
  "use strict";

  // swiper-testimonials
  new Swiper(".swiper-testimonials", {
    slidesPerView: 1,
    loop: true,
    spaceBetween: 50,
    speed: 300,
    autoplay: {
      delay: 5000,
    },
    navigation: {
      nextEl: ".testimonials-button-next",
      prevEl: ".testimonials-button-prev",
    },
  });

  // video play button
  var videoPlay = document.querySelectorAll(".video-play-btn");
  videoPlay.forEach(function (video) {
    video.addEventListener("click", function () {
      var thumbnail = this.parentNode.children;
      var thumbheight = thumbnail[1].height;
      var video =
        '<div class="ratio ratio-16x9 mx-auto bg-dark rounded-2 overflow-hidden" style="max-height:' +
        thumbheight +
        'px"><iframe style="max-height:' +
        thumbheight +
        'px" src="' +
        this.getAttribute("data-video-src") +
        "?autoplay=1&amp;modestbranding=1&amp;showinfo=0" +
        '" allowscriptaccess="always" allow="autoplay" allowfullscreen></iframe></div>';
      this.parentNode.innerHTML = video;
    });
  });

  // our_values_swiper slider
  new Swiper(".our_values_swiper", {
    loop: true,
    spaceBetween: 30,
    speed: 1500,
    autoplay: true,
    slidesPerView: 3,
    breakpoints: {
      320: {
        spaceBetween: 20,
        slidesPerView: 1,
      },
      575: {
        spaceBetween: 20,
        slidesPerView: 2,
      },
      1200: {
        slidesPerView: 3,
      },
    },
  });

  // integration slider
  new Swiper(".integration-swiper", {
    loop: true,
    spaceBetween: 0,
    centeredSlides: true,
    loop: true,
    speed: 3000,
    freeMode: true,
    simulateTouch: false,
    autoplay: {
      delay: 0,
      disableOnInteraction: false,
    },
    effect: "coverflow",
    coverflowEffect: {
      rotate: 0,
      stretch: 0,
      depth: 0,
      depthY: 30,
      modifier: 1,
      slideShadows: false,
    },
    slidesPerView: 4,
    breakpoints: {
      320: {
        spaceBetween: 20,
        slidesPerView: 4,
      },
      400: {
        slidesPerView: 4,
        spaceBetween: 30,
      },
      500: {
        slidesPerView: 5,
      },
      600: {
        slidesPerView: 6,
      },
      800: {
        slidesPerView: 7,
      },
      1000: {
        slidesPerView: 8,
      },
      1200: {
        slidesPerView: 9,
      },
      1400: {
        slidesPerView: 10,
      },
      1500: {
        slidesPerView: 11,
      },
      1600: {
        slidesPerView: 13,
      },
    },
  });
})();
