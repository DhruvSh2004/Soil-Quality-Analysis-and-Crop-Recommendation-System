document.querySelectorAll('.reclinks').forEach(item => {
    item.addEventListener('click', function() {
        const targetId = this.getAttribute('.accordion');
        
        const targetSection = document.getElementById(targetId);

        targetSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'  
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const accordions = document.querySelectorAll('.accordion');

    accordions.forEach(function (accordion) {
        accordion.addEventListener('click', function () {

            const panel = this.nextElementSibling;

            if (panel.classList.contains('open')) {
                panel.classList.remove('open');
            } else {

                document.querySelectorAll('.panel').forEach(function (p) {
                    p.classList.remove('open'); 
                });


                panel.classList.add('open');
            }
        });
    });
});

window.addEventListener('load', function() {
    const picText = document.querySelector('.pictext1');
    if (picText) { 
        setTimeout(() => {
            picText.classList.add('show'); 
        }, 1500);
    } else {
        console.log('Element not found'); 
    }
});
window.addEventListener('load', function() {
    const picpara = document.querySelector('.paradiv1');
    if (picpara) { 
        setTimeout(() => {
            picpara.classList.add('show'); 
        }, 1500);
    } else {
        console.log('Element not found'); 
    }
});

function updateFileName() {
    const fileInput = document.getElementById('cropFile');
    const fileNameDisplay = document.getElementById('file-name');

    if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = fileInput.files[0].name;
    } else {
        fileNameDisplay.textContent = "No file chosen";
    }
}

document.getElementById("uploadForm").addEventListener("submit", function (event) {
    const fileInput = document.getElementById("cropFile");
    const fileNameDisplay = document.getElementById("file-name");

    if (fileInput.files.length === 0) {
        fileNameDisplay.textContent = "No file chosen";
        
        event.preventDefault();
    }
});

// Save the scroll position before the page reloads
window.addEventListener("beforeunload", function () {
    sessionStorage.setItem("scrollPosition", window.scrollY);
});

// Restore the scroll position after the page loads
window.addEventListener("load", function () {
    const scrollPosition = sessionStorage.getItem("scrollPosition");
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition, 10));
        sessionStorage.removeItem("scrollPosition"); // Clean up
    }
});
