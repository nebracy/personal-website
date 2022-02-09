const navDropdown = document.getElementById("dropdown");
const navHamburger = document.getElementById("hamburger");
const screenOverlay = document.getElementById("overlay");
const maxWidth = window.matchMedia("(max-width: 650px)");

function checkScreenSize() {
    if (navDropdown.classList.contains("nav__menu--show")) {
        navDropdown.classList.remove("nav__menu--show");
        navHamburger.classList.remove("nav__hamburger--x");
        screenOverlay.classList.remove("screen-overlay--dim");
    }
}

document.addEventListener("click", e => {
    if (e.target.closest("#dropbtn") && maxWidth.matches) {    // Screen less than 650px
        navDropdown.classList.toggle("nav__menu--show");
        navHamburger.classList.toggle("nav__hamburger--x");
        screenOverlay.classList.toggle("screen-overlay--dim");
      } else if (maxWidth.matches) {
            checkScreenSize();
      }
});


const slider = document.getElementById('thickness_factor');

//Display the slider value
function updateSliderValue() {

    var sliderValue  = slider.value;
    document.getElementsByName("tf")[0].textContent = (sliderValue);
}

slider.addEventListener("change", updateSliderValue);

maxWidth.addEventListener("change", checkScreenSize);