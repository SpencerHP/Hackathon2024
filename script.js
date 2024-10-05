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

  function importExcel(sheetNumber) {
    const fileInput = document.getElementById(`import-file-${sheetNumber}`);
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file to import.");
        return;
    }

    const reader = new FileReader();

    reader.onload = function (event) {
        const data = new Uint8Array(event.target.result);
        const workbook = XLSX.read(data, { type: "array" });

        // Get the first sheet (you can modify this to select other sheets)
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];

        // Convert the sheet to JSON
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        console.log("Imported data:", jsonData); // Log the imported data
        
        // Set the data to the corresponding Handsontable instance
        if (sheetNumber === 1) {
            hot1.loadData(jsonData);
        } else if (sheetNumber === 2) {
            hot2.loadData(jsonData);
        }
    };

    reader.onerror = function () {
        alert("Error reading file. Please try again.");
    };

    reader.readAsArrayBuffer(file); // Read the file as an ArrayBuffer
}
