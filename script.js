document.getElementById("dropbtn").onclick = toggleDropdown;
document.getElementById("dropdown").onclick = toggleDropdown;

function toggleDropdown() {
    var x = window.matchMedia("(max-width: 650px)");
    if (x.matches) {
        document.getElementById("dropdown").classList.toggle("nav__menu--show");
    }
}
