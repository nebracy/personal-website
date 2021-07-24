const navDropdown = document.getElementById("dropdown");
const navHamburger = document.getElementById("hamburger");
const screenOverlay = document.getElementById("overlay");
const maxWidth = window.matchMedia("(max-width: 650px)");

function toggleDropdown(event) {
    if (event.target.closest("#dropbtn") && maxWidth.matches) {    // Screen less than 650px
        navDropdown.classList.toggle("nav__menu--show");
        navHamburger.classList.toggle("nav__hamburger--x");
        screenOverlay.classList.toggle("screen-overlay--dim");
      } else if (maxWidth.matches && navDropdown.classList.contains("nav__menu--show")) {
            navDropdown.classList.remove("nav__menu--show");
            navHamburger.classList.remove("nav__hamburger--x");
            screenOverlay.classList.remove("screen-overlay--dim");
      }
}

function checkScreenSize(event) {
    if (!event.matches && navDropdown.classList.contains("nav__menu--show")) {     // Screen (greater/not less) than 650px
        navDropdown.classList.remove("nav__menu--show");
        navHamburger.classList.remove("nav__hamburger--x");
        screenOverlay.classList.remove("screen-overlay--dim");
    }
}

document.addEventListener("click", toggleDropdown)
maxWidth.addEventListener("change", checkScreenSize)