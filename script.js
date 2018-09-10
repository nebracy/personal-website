document.addEventListener("click", toggleDropdown)

function toggleDropdown(event) {
    if (event.target.closest("#dropbtn")) {
        var width = window.matchMedia("(max-width: 650px)");    // Less than 650px
        if (width.matches) {
            document.getElementById("dropdown").classList.toggle("nav__menu--show");
        }
    } else {
        var element = document.getElementById("dropdown");
        if (element.classList.contains("nav__menu--show")) {
            element.classList.remove("nav__menu--show");
    }
}
}

function checkScreenSize() {
    var width = window.matchMedia("(min-width: 650px)");
    width.addListener(checkScreenSize);
    if (width.matches) {     // Greater than 650px
        var element = document.getElementById("dropdown");
        if (element.classList.contains("nav__menu--show")) {
            element.classList.remove("nav__menu--show");
        }
    }
}

checkScreenSize()
