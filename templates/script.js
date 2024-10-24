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