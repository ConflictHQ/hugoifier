'use strict';

// searchToggler keyboard shortcut
const searchToggler = document.querySelectorAll('[data-search-toggler]');
searchToggler.forEach((item) => {
	let userAgentData = navigator?.userAgentData?.platform || navigator?.platform || 'unknown';

	if (userAgentData == 'macOS') {
		item.innerText = `⌘ + K`
	} else {
		item.innerText = `Ctrl + K`
	}
});

// Navbar fixed
window.onscroll = function () {
	if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
		document.querySelector(".navigation").classList.add("nav-bg");
	} else {
		document.querySelector(".navigation").classList.remove("nav-bg");
	}
};

// Search wrapper show on
function isScrolledIntoView(el) {
	var rect = el.getBoundingClientRect();
	var elemTop = rect.top;
	var elemBottom = rect.bottom;

	// Only completely visible elements return true:
	var isVisible = (elemTop >= 0) && (elemBottom <= window.innerHeight);
	// Partially visible elements return true:
	//isVisible = elemTop < window.innerHeight && elemBottom >= 0;
	return isVisible;
}

window.addEventListener("scroll", function () {
	let header = document.querySelector("header");
	let banner_searchWrapper = document.querySelector("#banner .search-wrapper");
	let header_searchWrapper = document.querySelector("header .search-wrapper");

	try {
		if (isScrolledIntoView(banner_searchWrapper)) {
			header.classList.remove("search-active");
		} else {
			header.classList.add("search-active");
		}
	} catch (error) {

	}

});

// copy to clipboard
let blocks = document.querySelectorAll("pre");
blocks.forEach((block) => {
	if (navigator.clipboard) {
		let button = document.createElement("span");
		button.innerText = "copy";
		button.className = "copy-to-clipboard";
		block.appendChild(button);
		button.addEventListener("click", async () => {
			await copyCode(block, button);
		});
	}
});
async function copyCode(block, button) {
	let code = block.querySelector("code");
	let text = code.innerText;
	await navigator.clipboard.writeText(text);
	button.innerText = "copied";
	setTimeout(() => {
		button.innerText = "copy";
	}, 700);
}