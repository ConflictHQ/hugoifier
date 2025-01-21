// Passive event listeners
jQuery.event.special.touchstart = {
  setup: function (_, ns, handle) {
    this.addEventListener("touchstart", handle, {
      passive: !ns.includes("noPreventDefault"),
    });
  },
};
jQuery.event.special.touchmove = {
  setup: function (_, ns, handle) {
    this.addEventListener("touchmove", handle, {
      passive: !ns.includes("noPreventDefault"),
    });
  },
};

// prelaoder
$(window).on("load", function () {
  $(".preloader").fadeOut(10);
  AOS.init({
    once: true,
    anchorPlacement: "top-bottom",
  });
});

$(document).ready(function () {
  "use strict";

  // scroll-to-top-btn
  $(".scroll-to-top-btn").on("click", function () {
    $("html, body").animate({ scrollTop: 0 });
  });

  // scroll function
  $(window).on("scroll", function () {
    // counterUp
    function counter() {
      var oTop;
      if ($(".jsCounter").length !== 0) {
        oTop = $(".jsCounter").offset().top - window.innerHeight;
      }
      if ($(window).scrollTop() > oTop) {
        $(".jsCounter").each(function () {
          var $this = $(this),
            countTo = $this.attr("data-count");
          $({ countNum: $this.text() }).animate(
            { countNum: countTo },
            {
              duration: 500,
              easing: "swing",
              step: function () {
                $this.text(Math.floor(this.countNum));
              },
              complete: function () {
                $this.text(this.countNum);
              },
            }
          );
        });
      }
    }
    counter();
  });

  // tab
  $(".tab-content")
    .find(".tab-pane")
    .each(function (idx, item) {
      var navTabs = $(this).closest(".code-tabs").find(".nav-tabs"),
        title = $(this).attr("title");
      navTabs.append(
        '<li class="nav-item"><a class="nav-link" href="#">' +
          title +
          "</a></li>"
      );
    });

  $(".code-tabs ul.nav-tabs").each(function () {
    $(this).find("li:first").addClass("active");
  });

  $(".code-tabs .tab-content").each(function () {
    $(this).find("div:first").addClass("active");
  });

  $(".nav-tabs a").click(function (e) {
    e.preventDefault();
    var tab = $(this).parent(),
      tabIndex = tab.index(),
      tabPanel = $(this).closest(".code-tabs"),
      tabPane = tabPanel.find(".tab-pane").eq(tabIndex);
    tabPanel.find(".active").removeClass("active");
    tab.addClass("active");
    tabPane.addClass("active");
  });

  //single slider
  $(".single-slider").slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    dots: false,
    arrows: true,
    prevArrow:
      "<button type='button' class='prevArrow'><i class='fas fa-angle-left'></i></button>",
    nextArrow:
      "<button type='button' class='nextArrow'><i class='fas fa-angle-right'></i></button>",
  });

  // brandCarousel fix
  $(".brand-carousel").slick({
    dots: false,
    arrows: false,
    infinite: true,
    speed: 500,
    autoplay: true,
    autoplaySpeed: 3000,
    mobileFirst: true,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 1200,
        settings: {
          slidesToShow: 6,
        },
      },
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 5,
        },
      },
      {
        breakpoint: 767,
        settings: {
          slidesToShow: 4,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 3,
        },
      },
      {
        breakpoint: 0,
        settings: {
          slidesToShow: 2,
        },
      },
    ],
  });

  // tab slider
  function tabSliderInit() {
    $(".tab-slider").slick({
      infinite: true,
      slidesToShow: 3,
      slidesToScroll: 3,
      autoplay: false,
      dots: false,
      arrows: true,
      prevArrow:
        "<button type='button' class='prevArrow'><i class='fas fa-angle-left'></i></button>",
      nextArrow:
        "<button type='button' class='nextArrow'><i class='fas fa-angle-right'></i></button>",
      responsive: [
        {
          breakpoint: 1200,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2,
          },
        },
        {
          breakpoint: 767,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: true,
            arrows: false,
          },
        },
      ],
    });
  }
  tabSliderInit();

  $('[data-bs-toggle="pill"]').on("shown.bs.tab", function (e) {
    $(".tab-slider").slick("setPosition");
  });

  //post slider
  $(".post-slider").slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    dots: false,
    arrows: true,
    prevArrow:
      "<button type='button' class='prevArrow'><i class='fas fa-angle-left'></i></button>",
    nextArrow:
      "<button type='button' class='nextArrow'><i class='fas fa-angle-right'></i></button>",
  });
});
