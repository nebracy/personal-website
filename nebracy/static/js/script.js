document.addEventListener("click", toggleDropdown)

function toggleDropdown(event) {
    var element = document.getElementById("dropdown");
    var width = window.matchMedia("(max-width: 650px)");
    if (event.target.closest("#dropbtn") && width.matches) {    // Screen less than 650px
        element.classList.toggle("nav__menu--show");
      }
}

function checkScreenSize() {
    var width = window.matchMedia("(min-width: 650px)");
    width.addEventListener("change", checkScreenSize);
    if (width.matches) {     // Greater than 650px
        var element = document.getElementById("dropdown");
        if (element.classList.contains("nav__menu--show")) {
            element.classList.remove("nav__menu--show");
        }
    }
}

checkScreenSize()
