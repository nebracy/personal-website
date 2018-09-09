document.getElementById("dropbtn").onclick = toggleDropdown;
document.getElementById("dropdown").onclick = toggleDropdown;

function toggleDropdown() {
    var x = window.matchMedia("(max-width: 650px)");    // Less than 650px
    if (x.matches) {
        document.getElementById("dropdown").classList.toggle("nav__menu--show");
    }
}

function screenSize() {
    var width = window.matchMedia("(min-width: 650px)");
    width.addListener(screenSize);
    if (width.matches) {     // Greater than 650px
        var element = document.getElementById("dropdown");
        if (element.classList.contains("nav__menu--show")) {
            element.classList.remove("nav__menu--show");
        }
    }
}

screenSize()