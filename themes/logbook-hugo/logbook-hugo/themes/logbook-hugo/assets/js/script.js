(function () {
  ("use strict");

  // header search panel
  const navbar_collapse = document.querySelector(".navbar-collapse");
  const navbar_toggler = document.querySelector(".navbar-toggler");
  const header_search_panel = document.querySelector(".header-search-panel");
  const open_header_search_panel = document.querySelectorAll(
    '[data-target="open-header-search-panel"]'
  );
  const close_header_search_panel = document.querySelectorAll(
    '[data-target="close-header-search-panel"]'
  );

  if (header_search_panel) {
    open_header_search_panel.forEach((item) => {
      item.addEventListener("click", function () {
        header_search_panel.classList.add("show");
        navbar_collapse.classList.remove("show");
        navbar_toggler.classList.add("collapsed");
        navbar_toggler.setAttribute("aria-expanded", "false");
        setTimeout(() => {
          header_search_panel.querySelector("input").focus();
        }, 100);
      });
    });
    close_header_search_panel.forEach((item) => {
      item.addEventListener("click", function () {
        header_search_panel.classList.remove("show");
      });
    });
  }

  // back to top button
  document.querySelector("#scrollTop")?.addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });

  //post slider
  let post_sliders = document.querySelectorAll(".post-slider");
  if (post_sliders[0]) {
    for (let index = 0; index < post_sliders.length; index++) {
      new Swiper(post_sliders[index], {
        slidesPerView: 1,
        spaceBetween: 30,
        autoplay: {
          delay: 5000,
        },
        navigation: {
          nextEl: ".post-slider .swiper-button-next",
          prevEl: ".post-slider .swiper-button-prev",
        },
      });
    }
  }

  // featured post slider
  new Swiper(".featured-post-slider", {
    slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
    autoplay: {
      delay: 5000,
    },
    navigation: {
      nextEl: ".featured-post-slider .swiper-button-next",
      prevEl: ".featured-post-slider .swiper-button-prev",
    },
    pagination: {
      el: ".featured-post-slider .swiper-pagination",
      clickable: true,
    },
  });

  // product Slider Pagination
  let product_silder_pagination = new Swiper(
    ".single-product-slider-pagination",
    {
      slidesPerView: "auto",
    }
  );

  // product Slider
  new Swiper(".single-product-slider", {
    slidesPerView: 1,
    spaceBetween: 30,
    thumbs: {
      swiper: product_silder_pagination,
    },
  });
})();
