const element = document.getElementById("dropdown");
const minWidth = window.matchMedia("(min-width: 650px)");

function toggleDropdown(event) {
    var width = window.matchMedia("(max-width: 650px)");
    if (event.target.closest("#dropbtn") && width.matches) {    // Screen less than 650px
        element.classList.toggle("nav__menu--show");
      }
}

function checkScreenSize(event) {
    if (event.matches) {     // Screen greater than 650px
        if (element.classList.contains("nav__menu--show")) {
            element.classList.remove("nav__menu--show");
        }
    }
}

document.addEventListener("click", toggleDropdown)
minWidth.addEventListener("change", checkScreenSize)