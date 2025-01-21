(function () {
  "use strict";

  // Preloader js
  window.addEventListener("load", function () {
    document.querySelector(".preloader").style.display = "none";
  });

  // Element Existence checker function
  function elementExistenceChecker(element) {
    if (element) {
      return true;
    } else {
      return false;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
      // -----------------------------
      //  Testimonial Slider
      // ----------------------------- 
      new Swiper(".testimonial-slider", {
        loop: true,
        slidesPerView: 2,
        spaceBetween: 30,
        pagination: {
          el: ".testimonial-slider .swiper-pagination",
          clickable: true,
        },
        breakpoints: {
          0: {
            slidesPerView: 1,
            spaceBetween: 20
          },
          768: {
            slidesPerView: 2,
            spaceBetween: 20
          }
        }
      });

      // -----------------------------
      new Swiper(".about-slider", {
        loop: true,
        slidesPerView: 1,
        centeredSlides: true,
        pagination: {
          el: ".about-slider .swiper-pagination",
          clickable: true,
        },
      });

      // -----------------------------
      new Swiper(".quote-slider", {
        loop: true,
        slidesPerView: 1,
        centeredSlides: true,
        autoplay: true,
        pagination: {
          el: ".quote-slider .swiper-pagination",
          clickable: true,
        },
      });

      // -----------------------------
      //  Client Slider
      // -----------------------------  
      new Swiper(".client-slider", {
        loop: true,
        slidesPerView: 1,
        autoplay: true,
        spaceBetween: 60,
        pagination: {
          el: ".client-slider .swiper-pagination",
          clickable: true,
        },
        breakpoints: {
          0: {
            slidesPerView: 1,
          },
          400: {
            slidesPerView: 2,
          },
          1000: {
            slidesPerView: 4,
          },
        }
      });
    }, 500);

    // -----------------------------
    //  Video Replace
    // -----------------------------
    let video = document.querySelector(".video");
    let videoBtn = document.querySelector(".video-box i");
    let videoReplace = document.querySelector(".video-box > a");

    if (elementExistenceChecker(videoBtn)) {
      videoBtn.addEventListener("click", function () {
        let videoLink = videoBtn.getAttribute("data-video");
        let video = '<iframe allowfullscreen src="' + videoLink + '"></iframe>';
        videoReplace.innerHTML = video;
      });
    };

    // -----------------------------
    //  Video Modal Popup
    // -----------------------------
    let videoModalBtn = document.querySelector(".video-modal-btn");
    let videoModal = document.querySelector("#videoModal");
    let videoModalIframe = document.querySelector("#video");
    let videoLink = (() => {
      if (elementExistenceChecker(videoModalBtn)) {
        return videoModalBtn.getAttribute("data-src");
      }
    })();

    if (elementExistenceChecker(videoModalBtn)) {
      videoModalBtn.addEventListener("click", function () {
        if (elementExistenceChecker(videoModalIframe)) {
          videoModalIframe.setAttribute("src", videoLink);
        }

        if (elementExistenceChecker(videoModal)) {
          videoModal.addEventListener("shown.bs.modal", function () {
            videoModalIframe.setAttribute("src", videoLink + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
          });

          videoModal.addEventListener("hide.bs.modal", function () {
            videoModalIframe.setAttribute("src", "");
          });
        }
      });
    }

    // ----------------------------
    // AOS
    // ----------------------------
    AOS.init({
      once: true
    });
  });

})();