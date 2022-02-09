const navDropdown = document.getElementById("dropdown");
const navHamburger = document.getElementById("hamburger");
const screenOverlay = document.getElementById("overlay");
const maxWidth = window.matchMedia("(max-width: 650px)");

const slider = document.getElementById('thickness_factor');
const radioChoice = document.getElementById('choice');


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


function updateSliderValue() {

    var sliderValue  = slider.value;
    document.getElementsByName("tf")[0].textContent = (sliderValue);
}


function tfWeight() {
    if (document.getElementById('choice-0').checked) {
        document.getElementById('choice-weight').style.display = "block";
        document.getElementById('choice-tf').style.display = "none";
    }
    else {
        document.getElementById('choice-weight').style.display = "none";
        document.getElementById('choice-tf').style.display = "block";
    }
}

radioChoice.addEventListener("change", tfWeight);

slider.addEventListener("change", updateSliderValue);

maxWidth.addEventListener("change", checkScreenSize);