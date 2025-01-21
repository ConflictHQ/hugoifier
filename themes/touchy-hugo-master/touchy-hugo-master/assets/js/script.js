function toggleNavbar() {
  navbar.classList.toggle("opened");
  const isOpened = navbar.classList.contains("opened");
  navbarToggle.setAttribute("aria-label", isOpened ? "Close navigation menu." : "Open navigation menu.");
}

function openMobileNavbar() {
  navbar.classList.add("opened");
  navbarToggle.setAttribute("aria-label", "Close navigation menu.");
}

function closeMobileNavbar() {
  navbar.classList.remove("opened");
  navbarToggle.setAttribute("aria-label", "Open navigation menu.");
}

function stopPropagation(clickEvent) {
  clickEvent.stopPropagation();
}

let navbar = document.querySelector(".navbar");
let navbarToggle = navbar.querySelector(".navbar-toggle");
let navbarMenu = navbar.querySelector(".navbar-menu");
let navbarLinksContainer = navbar.querySelector(".navbar-links");

navbarToggle.addEventListener("click", toggleNavbar);
navbarLinksContainer.addEventListener("click", stopPropagation);
navbarMenu.addEventListener("click", closeMobileNavbar);
