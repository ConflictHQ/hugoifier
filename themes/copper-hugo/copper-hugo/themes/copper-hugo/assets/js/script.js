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

// preloader
$(window).bind("load", function () {
  function preLoader() {
    $("body").addClass("loaded");
    if ($(".preloader").length !== 0) {
      $(".preloader").addClass("loaded");
    }
  }
  setTimeout(function () {
    preLoader();
  }, 600);
});

// on ready state
(function ($) {
  "use strict";

  // counterUp
  document.addEventListener("DOMContentLoaded", function () {
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
  });

  // inCircle element
  function inCircleInit() {
    if ($(window).width() > 575) {
      var oTop;
      if ($("#inCircle-element").length !== 0) {
        oTop = $("#inCircle-element").offset().top - window.innerHeight;
      }
      if ($(window).scrollTop() > oTop) {
        $("#inCircle-element").incircle({
          radius: "13.5em", //distance from center
          start: -150,
        });
      }
    }
  }

  $(window).on("scroll", function () {
    if ($(".jsCounter").length !== 0) {
      counter();
    }
    if ($(".jsCounter-2").length !== 0) {
      counterTwo();
    }
    inCircleInit();

    if ($(".scroll-to-top-btn").length !== 0) {
      // scroll to top
      var scrollToTop = $(".scroll-to-top-btn"),
        scroll = $(window).scrollTop();

      if (scroll >= 400) {
        scrollToTop.addClass("show");
      } else {
        scrollToTop.removeClass("show");
      }
    }
  });

  // scroll to top button
  if ($(".scroll-to-top-btn").length !== 0) {
    $(".scroll-to-top-btn").on("click", function (e) {
      e.preventDefault();
      $("html, body").animate(
        {
          scrollTop: 0,
        },
        0
      );
    });
  }

  // aos scroll-animation Init
  window.addEventListener("load", () => {
    AOS.init({
      duration: 600,
      once: true,
    });
  });

  $(document).ready(function () {
    if ($(window).width() < 1199) {
      $(".navbar .dropdown-toggle").on("click", function (e) {
        $(this).siblings(".dropdown-menu, .dropdown-submenu").animate(
          {
            height: "toggle",
          },
          300
        );
      });
    }

    // disable accordion collapse toogle
    $(".disable-toogle").on("hide.bs.collapse", function (e) {
      e.preventDefault();
    });

    // popupFix init
    function popupFix() {
      var vScrollWidth = window.innerWidth - $(document).width();
      function noBodyScroll() {
        $("body").css({
          "padding-right": vScrollWidth + "px",
          "overflow-y": "hidden",
        });
      }
      function doBodyScroll() {
        setTimeout(function () {
          $("body").css({
            "padding-right": 0,
            "overflow-y": "auto",
          });
        }, 300);
      }
      var navbarToggler = $(".navbar-toggler");
      $(navbarToggler).on("click", function () {
        if (navbarToggler.attr("aria-expanded") === "false") {
          doBodyScroll();
        }
        if (navbarToggler.attr("aria-expanded") === "true") {
          noBodyScroll();
        }
      });
    }
    popupFix();

    // horizontalAccordion init
    function horizontalAccordion() {
      $(".horizontal-accordion-item").on("click", function () {
        $(this).addClass("active").siblings().removeClass("active");
      });
    }
    horizontalAccordion();

    // smoothScroll init
    function smoothScroll() {
      $(".smooth-scroll").click(function (event) {
        if (
          location.pathname.replace(/^\//, "") ===
            this.pathname.replace(/^\//, "") &&
          location.hostname === this.hostname
        ) {
          var target = $(this.hash);
          target = target.length
            ? target
            : $("[name=" + this.hash.slice(1) + "]");
          if (target.length) {
            event.preventDefault();
            $("html, body").animate(
              {
                scrollTop: target.offset().top,
              },
              300,
              function () {
                var $target = $(target);
                $target.focus();
                if ($target.is(":focus")) {
                  return false;
                } else {
                  $target.attr("tabindex", "-1");
                  $target.focus();
                }
              }
            );
          }
        }
      });
    }
    smoothScroll();

    if ($(".pricing-check").length !== 0) {
      // pricing init
      function pricingInit() {
        var toggleSwitch = $(".pricing-check");
        var number = $(".data-count");
        $(toggleSwitch).change(function () {
          if ($(toggleSwitch).is(":checked")) {
            $(".data-count").each(function () {
              $(this).html($(this).data("count-annually"));
              $(this)
                .prop("Counter", 0)
                .animate(
                  {
                    Counter: $(this).text(),
                  },
                  {
                    duration: 250,
                    easing: "swing",
                    step: function (now) {
                      $(this).text(Math.ceil(now));
                    },
                  }
                );
            });
            $(".text-monthly").addClass("d-none").removeClass("d-inline");
            $(".text-annually").addClass("d-inline").removeClass("d-none");
          } else if ($(toggleSwitch).is(":not(:checked)")) {
            $(".data-count").each(function () {
              $(this).html($(this).data("count-monthly"));
              $(this)
                .prop("Counter", 0)
                .animate(
                  {
                    Counter: $(this).text(),
                  },
                  {
                    duration: 250,
                    easing: "swing",
                    step: function (now) {
                      $(this).text(Math.ceil(now));
                    },
                  }
                );
            });
            $(".text-monthly").addClass("d-inline").removeClass("d-none");
            $(".text-annually").addClass("d-none").removeClass("d-inline");
          }
        });
      }
      pricingInit();
    }

    // brandCarousel fix
    if ($(".brand-carousel").length !== 0) {
      function brandCarousel() {
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
      }
      brandCarousel();
    }

    // testimonialsCarousel fix
    if ($(".testimonials-carousel").length !== 0) {
      function testimonialsCarousel() {
        $(".testimonials-carousel").slick({
          dots: true,
          arrows: false,
          infinite: true,
          speed: 400,
          slidesToShow: 3,
          slidesToScroll: 1,
          responsive: [
            {
              breakpoint: 991,
              settings: {
                slidesToShow: 2,
              },
            },
            {
              breakpoint: 767,
              settings: {
                slidesToShow: 1,
              },
            },
          ],
        });
      }
      testimonialsCarousel();
    }

    // videoPopupInit
    if ($(".video-play-btn").length !== 0) {
      function videoPopupInit() {
        var $videoSrc;
        $(".video-play-btn").click(function () {
          $videoSrc = $(this).data("src");
        });
        $("#videoModal").on("shown.bs.modal", function (e) {
          $("#showVideo").attr(
            "src",
            $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0"
          );
        });
        $("#videoModal").on("hide.bs.modal", function (e) {
          $("#showVideo").attr("src", $videoSrc);
        });
      }
      videoPopupInit();
    }

    // masonryFilter init
    var containerEl = document.querySelector("#masonry");
    if (containerEl) {
      setTimeout(() => {
        var Shuffle = window.Shuffle;
        var myShuffle = new Shuffle(document.querySelector("#masonry"), {
          itemSelector: ".masonry-item",
          buffer: 1,
        });
        jQuery('input[name="shuffle-filter"]').on("change", function (evt) {
          var input = evt.currentTarget;
          if (input.checked) {
            myShuffle.filter(input.value);
          }
        });
        $("input[name='shuffle-filter']").on("click", function () {
          $(this).parent().addClass("active").siblings().removeClass("active");
        });
      }, 1000);
    }
  });

  // Form validation Init
  if ($(".needs-validation").length !== 0) {
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
  }
})(jQuery);

// integrated tools
(function ($) {
  "use strict";
  $.fn.incircle = function (options) {
    var settings = $.extend(
      {
        color: "#556b2f",
        backgroundColor: "white",
        type: 1, //circle type - 1 whole, 0.5 half, 0.25 quarter
        radius: "14em", //distance from center
        start: 0, //shift start from 0
        top: "0",
        left: "0",
      },
      options
    );
    this.css({
      position: "relative",
      top: settings.top,
      left: settings.left,
      "list-style-type": "none",
      margin: 0,
    });
    var elements = this.children(":not(:first-child)");
    var numberOfElements =
      settings.type === 1 ? elements.length : elements.length - 1;
    var slice = (360 * settings.type) / numberOfElements;
    elements.each(function (i) {
      var $self = $(this),
        rotate = slice * i + settings.start,
        rotateReverse = rotate * -1;
      $self.css({
        position: "absolute",
        "-webkit-transition": "all 1s linear",
        "-moz-transition": "all 1s linear",
        transition: "all 1s linear",
      });
      $self.css({
        transform:
          "rotate(" +
          rotate +
          "deg) translate(" +
          settings.radius +
          ") rotate(" +
          rotateReverse +
          "deg)",
      });
    });
    return this;
  };
})(jQuery);
