var tablinks = document.getElementsByClassName("tab-links");
var tabcontents = document.getElementsByClassName("tab-contents");

function opentab(tabname){
    for(tablink of tablinks){
        tablink.classList.remove("active-link");
    }

    for(tabcontent of tabcontents){
        tabcontent.classList.remove("active-tab");
    }

    event.currentTarget.classList.add("active-link");
    document.getElementById(tabname).classList.add("active-tab");
}

var sidemenu = document.getElementById("sidemenu");

function openmenu(){
    sidemenu.style.right = "0";
}
function closemenu(){
    sidemenu.style.right = "-200px";
}

// typing annimation scrpit
var typed = new Typed(".typing", {
    strings: ["A Huntington Product", "A Huntington Solution", "A Huntington Offering", "A Huntington Framework", "A Huntington Welcome"],
    typeSpeed: 100,
    backSpeed: 60,
    loop: true
});




function openForm1() {
    document.getElementById("myForm1").style.display = "block";
  }
  
  function closeForm1() {
    document.getElementById("myForm1").style.display = "none";
  }


function openForm2() {
    document.getElementById("myForm2").style.display = "block";
  }
  
  function closeForm2() {
    document.getElementById("myForm2").style.display = "none";
  }


  function submitForm(side) {
    let field1, field2;
    if (side === 'left') {
        field1 = document.getElementById('field1').value;
        field2 = document.getElementById('field2').value;
        alert(`Left Side:\nField 1: ${field1}\nField 2: ${field2}`);
    } else {
        field1 = document.getElementById('field3').value;
        field2 = document.getElementById('field4').value;
        alert(`Right Side:\nField 3: ${field1}\nField 4: ${field2}`);
    }
}