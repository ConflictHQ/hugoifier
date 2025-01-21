(function () {
  "use strict";

  window.addEventListener("load", () => {
    // Element Existence Checker Function
    function isElementExist(element) {
      if (element) {
        return true;
      }
      return false;
    }

    // Aos js 
    AOS.init({
      once: true,
      offset: 250,
      easing: 'ease',
      duration: 900
    });

    // ##################
    // Video Modal 
    // ##################
    let videoPlayBtn = document.querySelectorAll(".play-icon");
    let videoModal = document.querySelector("#videoModal");

    if (isElementExist(videoPlayBtn)) {
      videoPlayBtn.forEach((btn) => {
        btn.addEventListener("click", function () {
          let videoIframe = document.querySelector("#videoModal iframe");
          let videoLink = btn.getAttribute("video-url");
          videoIframe.setAttribute("src", videoLink);
        });
      });

      if (isElementExist(videoModal)) {
        videoModal.addEventListener("hidden.bs.modal", function () {
          let videoIframe = document.querySelector("#videoModal iframe");
          videoIframe.setAttribute("src", "");
        });
      }
    };

    // ##################
    // counterUp 
    // ##################
    // You can change this class to specify which elements are going to behave as counters.
    var elements = document.querySelectorAll(".counter");

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
    var isElementVisible = function isElementVisible(el) {
      var scroll = window.scrollY || window.pageYOffset;
      var boundsTop = el.getBoundingClientRect().top + scroll;
      var viewport = {
        top: scroll,
        bottom: scroll + window.innerHeight,
      };
      var bounds = {
        top: boundsTop,
        bottom: boundsTop + el.clientHeight,
      };
      return (
        (bounds.bottom >= viewport.top && bounds.bottom <= viewport.bottom) ||
        (bounds.top <= viewport.bottom && bounds.top >= viewport.top)
      );
    };

    // Funciton that will get fired uppon scrolling
    var handleScroll = function handleScroll() {
      elements.forEach(function (item, id) {
        if (true === item.counterAlreadyFired) return;
        if (!isElementVisible(item)) return;
        item.updateCounter();
        item.counterAlreadyFired = true;
      });
    };

    // Fire the function on scroll
    window.addEventListener("scroll", handleScroll);
  })

  // ##################
  // navfixed
  // ##################
  let scrolling = window.scrollY;
  let naviagtion = document.querySelector(".naviagtion");

  function navFixed() {
    scrolling = window.scrollY;

    if (scrolling > 10) {
      naviagtion.classList.add('nav-bg');
    } else {
      naviagtion.classList.remove('nav-bg');
    }
  };

  navFixed();
  window.addEventListener("scroll", (e) => {
    navFixed();
  })

  // ##################
  // testimonial
  // ##################
  new Swiper(".testimonial-slider", {
    slidesPerView: 3,
    loop: true,
    spaceBetween: 50,
    grabCursor: true,
    enteredSlides: true,
    speed: 900,
    autoplay: true,
    breakpoints: {
      // when window width is >= 0 px
      0: {
        slidesPerView: 1,
        spaceBetween: 40
      },
      // when window width is >= 768 px
      768: {
        slidesPerView: 2,
        spaceBetween: 50
      },
      // when window width is >= 991 px
      991: {
        slidesPerView: 3,
        spaceBetween: 50
      }
    }
  });

})();