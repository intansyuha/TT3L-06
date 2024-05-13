const labels = document.querySelectorAll('.accordion-row label');

// Initialize the display property of the accordion content
labels.forEach(label => {
  const accordionContent = label.nextElementSibling;
  accordionContent.style.display = 'none'; // Initialize to 'none'
});

// Add event listener to each label
labels.forEach(label => {
    label.addEventListener('click', () => {
        const accordionContent = label.nextElementSibling;
        const chevron = label.querySelector('i');

        // Toggle the display property of the accordion content
        accordionContent.style.display = accordionContent.style.display === 'flex' ? 'none' : 'flex';

        // Toggle the chevron icon
        chevron.classList.toggle('bx-chevron-right');
        chevron.classList.toggle('bx-chevron-down');
    });
});


document.addEventListener("DOMContentLoaded", function() {
  const navBar = document.querySelector("nav");
  const menuBtns = document.querySelectorAll(".menu-icon");
  const overlay = document.querySelector(".overlay");

  menuBtns.forEach((menuBtn) => {
    menuBtn.addEventListener("click", () => {
      navBar.classList.toggle("nav");
      navBar.classList.toggle("open");
    });
  });

  overlay.addEventListener("click", () => {
    navBar.classList.remove("nav");
    navBar.classList.remove("open");
  });
});

const smallBoxes = document.querySelectorAll('.small-box');
const fullSizedImage = document.querySelector('.full-sized-image');
const fullSizedImageImg = document.querySelector('.full-sized-image img');

smallBoxes.forEach((smallBox) => {
  smallBox.addEventListener('click', () => {
    const imgSrc = smallBox.querySelector('img').src;
    fullSizedImageImg.src = imgSrc;
    fullSizedImage.style.display = 'flex';
  });
});

document.addEventListener('click', (event) => {
  if (!event.target.closest('.small-box')) {
    fullSizedImage.style.display = 'none';
  }
});

const toggleSwitches = document.querySelectorAll('.toogle-switch');

toggleSwitches.forEach(switchElem => {
    switchElem.addEventListener("click", () => {
        switchElem.classList.toggle('active');
    });
});
