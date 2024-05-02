const dropdownLabels = document.querySelectorAll('.dropdown-row label');

dropdownLabels.forEach(label => {
    label.addEventListener('click', () => {
        const dropdownBox = label.nextElementSibling;
        dropdownBox.classList.toggle('show');
        
    })
})