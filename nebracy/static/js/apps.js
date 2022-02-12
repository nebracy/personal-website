const slider = document.getElementById('thk_factor');


function updateSliderValue() {
    var sliderValue  = slider.value;
    document.getElementsByName("tf")[0].textContent = (sliderValue);
}


function tfWeight() {
    doughWt = document.getElementById('dough_wt');
    pizzaSz = document.getElementById('pizza_size');

    if (document.getElementById('choice-0').checked) {
        document.getElementById('choice-wt').style.display = "block";
        document.getElementById('choice-tf').style.display = "none";
        pizzaSz.required = false;
        doughWt.required = true;
        pizzaSz.value = 16;

    }
    else {
        document.getElementById('choice-wt').style.display = "none";
        document.getElementById('choice-tf').style.display = "block";
        pizzaSz.required = true;
        doughWt.required = false;
        doughWt.value = "";
    }
}

tfWeight();


function printTable() {
     var divToPrint=document.getElementById("recipe");
        newWin= window.open("", "", 'height=500, width=750');
        newWin.document.write(divToPrint.outerHTML);
        newWin.print();
        newWin.close();
}


function hideShowPrint() {
    if (document.getElementById('recipe')) {
        document.getElementById('print').hidden = false;
    }
    else {
        document.getElementById('print').hidden = true;
    }
}

hideShowPrint();


document.getElementById("print").addEventListener("click", printTable);

document.getElementById('choice').addEventListener("change", tfWeight);

slider.addEventListener("input", updateSliderValue);