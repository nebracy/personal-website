const navDropdown = document.getElementById("dropdown");
const maxWidth = window.matchMedia("(max-width: 650px)");

function toggleDropdown(event) {
    if (event.target.closest("#dropbtn") && maxWidth.matches) {    // Screen less than 650px
        navDropdown.classList.toggle("nav__menu--show");
      }
}

function checkScreenSize(event) {
    if (!event.matches) {     // Screen (greater/not less) than 650px
        if (navDropdown.classList.contains("nav__menu--show")) {
            navDropdown.classList.remove("nav__menu--show");
        }
    }
}

document.addEventListener("click", toggleDropdown)
maxWidth.addEventListener("change", checkScreenSize)