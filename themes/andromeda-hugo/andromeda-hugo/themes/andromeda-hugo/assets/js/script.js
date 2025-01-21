var header = document.querySelector(".header-nav");
var lastScroll = 0;
window.onscroll = () => {
  // header-sticky-top
  if (window.pageYOffset >= 50) {
    header.classList.add("header-sticky-top");
  } else {
    header.classList.remove("header-sticky-top");
  }

  // headerPinUnpin init
  var currentScroll =
    document.documentElement.scrollTop || document.body.scrollTop;
  if (currentScroll > 300 && lastScroll <= currentScroll) {
    lastScroll = currentScroll;
    header.classList.add("header-unpinned");
  } else {
    lastScroll = currentScroll;
    header.classList.remove("header-unpinned");
  }
};

window.onload = () => {
  // Preloader init
  setTimeout(() => {
    document.querySelector(".preloader").classList.add("preloader-hide");
  }, 150);

  // AOS init
  setTimeout(() => {
    AOS.init({
      duration: 600,
      once: true,
    });
  }, 50);

  // video embed
  var videoPlay = document.querySelectorAll(".video-play-btn");
  videoPlay.forEach(function (video) {
    var thumbnail = video.nextElementSibling;
    var thumbWidth = thumbnail.width;
    video.addEventListener("click", function () {
      var videoEl =
        '<div class="ratio ratio-16x9 mx-auto bg-dark overflow-hidden" style="max-width:' +
        thumbWidth +
        'px"><iframe src="' +
        this.getAttribute("data-src") +
        "?autoplay=1&amp;modestbranding=1&amp;showinfo=0" +
        '" allowscriptaccess="always" allow="autoplay" allowfullscreen></iframe></div>';
      this.parentNode.innerHTML = videoEl;
    });
  });

  // rellax
  if (document.querySelectorAll("[data-rellax-speed]").length) {
    var rellax = new Rellax("[data-rellax-speed]");
  }

  // brand-carousel
  new Swiper(".brand-carousel", {
    spaceBetween: 0,
    speed: 1000,
    loop: true,
    autoplay: {
      delay: 3000,
    },
    breakpoints: {
      0: {
        slidesPerView: 2,
        spaceBetween: 0,
      },
      640: {
        slidesPerView: 3,
        spaceBetween: 0,
      },
      767: {
        slidesPerView: 3,
        spaceBetween: 0,
      },
      991: {
        slidesPerView: 5,
        spaceBetween: 0,
      },
    },
  });

  // featuresCarousel fix
  new Swiper(".features-carousel", {
    spaceBetween: 0,
    speed: 600,
    autoplay: true,
    breakpoints: {
      0: {
        slidesPerView: 1,
        spaceBetween: 0,
      },
      575: {
        slidesPerView: 1,
        spaceBetween: 0,
      },
      767: {
        slidesPerView: 2,
        spaceBetween: 0,
      },
      991: {
        slidesPerView: 3,
        spaceBetween: 0,
      },
    },
    pagination: {
      el: ".swiper-pagination",
      dynamicBullets: true,
      clickable: true,
    },
  });

  // testimonialsCarousel fix
  new Swiper(".testimonial-carousel", {
    spaceBetween: 0,
    speed: 600,
    loop: true,
    autoplay: true,
    slidesPerView: 1,
    pagination: {
      el: ".swiper-pagination",
      dynamicBullets: true,
      clickable: true,
    },
  });
};

// Form validation Init
(function () {
  window.addEventListener(
    "load",
    function () {
      var forms = document.getElementsByClassName("needs-validation");
      var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener(
          "submit",
          function (event) {
            if (form.checkValidity() === false) {
              event.preventDefault();
              event.stopPropagation();
            }
            form.classList.add("was-validated");
          },
          false
        );
      });
    },
    false
  );
})();
