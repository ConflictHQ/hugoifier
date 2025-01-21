(function () {
  "use strict";

  // Aos Animation
  // ----------------------------------------
  AOS.init({
    once: true,
    disable: "mobile",
  });

  // Make External Svg Into Inline Svg
  // ----------------------------------------
  let svgImages = document.querySelectorAll(".inline-svg");
  SVGInjector(svgImages);

  // Sticky Header
  // ----------------------------------------
  const header = document.querySelector("header.sticky-header");

  function stickyHeader() {
    header?.classList.toggle("header-fixed-top", window.pageYOffset > 0);
  }

  stickyHeader();
  window.addEventListener("scroll", stickyHeader);

  // Set the `scroll-margin-top` property for all elements that are referenced by the href values of anchor elements within the table of contents
  // ----------------------------------------
  function setHeaderScrollMarginTop() {
    const header = document.querySelector("header.sticky-header");

    if (header) {
      const tableOfContents = document.getElementById("TableOfContents");
      const anchors = tableOfContents?.querySelectorAll("a");
      const headerHeight = header.offsetHeight - 10;

      anchors?.forEach((anchor) => {
        const href = anchor.getAttribute("href");
        const targetElement = document.querySelector(href);

        if (targetElement) {
          targetElement.style.scrollMarginTop = `${headerHeight}px`;
        }
      });
    }
  }

  // Initial Call
  setHeaderScrollMarginTop();

  // Re-assign scroll-margin-top on window resize
  window.addEventListener("resize", setHeaderScrollMarginTop);

  // Navbar Toggler
  // ----------------------------------------
  const navbarToggler = document.querySelector(".navbar-toggler");
  const navbarMenu = document.querySelector(".navbar-wrapper");

  navbarToggler?.addEventListener("click", () => {
    navbarToggler.classList.toggle("active");
    navbarMenu.classList.toggle("active");
  });

  // Dropdown Menu Toggler For Mobile
  // ----------------------------------------
  const dropdownMenuToggler = document.querySelectorAll(
    ".nav-dropdown > .nav-link"
  );

  dropdownMenuToggler.forEach((toggler) => {
    toggler?.addEventListener("click", (e) => {
      e.target.parentElement.classList.toggle("active");
    });
  });

  // Animated Counter
  // ----------------------------------------
  document.addEventListener("DOMContentLoaded", function () {
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
        if (true === item.counterAlreadyFired) {
          return;
        }
        if (!isElementVisible(item)) {
          return;
        }
        item.updateCounter();
        item.counterAlreadyFired = true;
      });
    };

    // Fire the function on scroll
    window.addEventListener("scroll", handleScroll);
  });

  // Accordion
  // ----------------------------------------
  const accordion = document.querySelectorAll("[data-accordion]");
  accordion.forEach((header) => {
    header.addEventListener("click", () => {
      const accordionItem = header.parentElement;
      accordionItem.classList.toggle("active");
    });
  });

  // Announcement
  // ----------------------------------------
  const announcement = document.querySelector(".announcement");
  const announcementButton = document.querySelector(".announcement .close-btn");
  announcementButton?.addEventListener("click", () => {
    announcement.classList.add("hidden");
  });
})();
