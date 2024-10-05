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