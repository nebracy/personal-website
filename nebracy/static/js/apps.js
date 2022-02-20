
document.querySelectorAll('.slider').forEach(slider => {
    slider.addEventListener('input', function(e) {
         if (this.id == 'thk_factor') {
            document.getElementsByName("tf")[0].textContent = this.value;
        }
        else if (this.id == 'water') {
            document.getElementsByName("hydration")[0].textContent = this.value + "%";
        }
    })
})


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
