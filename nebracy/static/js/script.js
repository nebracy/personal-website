const navDropdown = document.getElementById("dropdown");
const navHamburger = document.getElementById("hamburger");
const maxWidth = window.matchMedia("(max-width: 650px)");

function toggleDropdown(event) {
    if (event.target.closest("#dropbtn") && maxWidth.matches) {    // Screen less than 650px
        navDropdown.classList.toggle("nav__menu--show");
        navHamburger.classList.toggle("nav__hamburger--active");
      } else if (maxWidth.matches && navDropdown.classList.contains("nav__menu--show")) {
            navDropdown.classList.remove("nav__menu--show");
            navHamburger.classList.remove("nav__hamburger--active");
      }
}

function checkScreenSize(event) {
    if (!event.matches && navDropdown.classList.contains("nav__menu--show")) {     // Screen (greater/not less) than 650px
        navDropdown.classList.remove("nav__menu--show");
        navHamburger.classList.remove("nav__hamburger--active");
    }
}

document.addEventListener("click", toggleDropdown)
maxWidth.addEventListener("change", checkScreenSize)