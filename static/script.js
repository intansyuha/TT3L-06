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


document.addEventListener("DOMContentLoaded", function () {
  const topSmallBoxes = document.querySelectorAll('#tops-accordion .small-box');
  const topContainer = document.querySelector('.top-container');
  const topContainerImg = document.querySelector('.top-container img');

  const bottomSmallBoxes = document.querySelectorAll('#bottoms-accordion .small-box');
  const bottomContainer = document.querySelector('.bottom-container');
  const bottomContainerImg = document.querySelector('.bottom-container img');

  const outerSmallBoxes = document.querySelectorAll('#outerwear-accordion .small-box');
  const outerContainer = document.querySelector('.outerwear-container');
  const outerContainerImg = document.querySelector('.outerwear-container img');

  const shoeSmallBoxes = document.querySelectorAll('#shoes-accordion .small-box');
  const shoeContainer = document.querySelector('.shoes-container');
  const shoeContainerImg = document.querySelector('.shoes-container img');

  const bagSmallBoxes = document.querySelectorAll('#bags-accordion .small-box');
  const bagContainer = document.querySelector('.bags-container');
  const bagContainerImg = document.querySelector('.bags-container img');

  const accSmallBoxes = document.querySelectorAll('#accessories-accordion .small-box');
  const accContainer = document.querySelector('.accessories-container');
  const accContainerImg = document.querySelector('.accessories-container img');

  

  topSmallBoxes.forEach((smallBox) => {
    smallBox.addEventListener('click', () => {
      const imgSrc = smallBox.querySelector('img').src;
      topContainerImg.src = imgSrc;
      topContainer.style.display = 'flex';
    });
  });

  bottomSmallBoxes.forEach((smallBox) => {
    smallBox.addEventListener('click', () => {
      const imgSrc = smallBox.querySelector('img').src;
      bottomContainerImg.src = imgSrc;
      bottomContainer.style.display = 'flex';
    });
  });
  
  outerSmallBoxes.forEach((smallBox) => {
    smallBox.addEventListener('click', () => {
      const imgSrc = smallBox.querySelector('img').src;
      outerContainerImg.src = imgSrc;
      outerContainer.style.display = 'flex';
    });
  });
  
  shoeSmallBoxes.forEach((smallBox) => {
    smallBox.addEventListener('click', () => {
      const imgSrc = smallBox.querySelector('img').src;
      shoeContainerImg.src = imgSrc;
      shoeContainer.style.display = 'flex';
    });
  });
  
  bagSmallBoxes.forEach((smallBox) => {
    smallBox.addEventListener('click', () => {
      const imgSrc = smallBox.querySelector('img').src;
      bagContainerImg.src = imgSrc;
      bagContainer.style.display = 'flex';
    });
  });

  accSmallBoxes.forEach((smallBox) => {
    smallBox.addEventListener('click', () => {
      const imgSrc = smallBox.querySelector('img').src;
      accContainerImg.src = imgSrc;
      accContainer.style.display = 'flex';
    });
  });


    topContainer.addEventListener('click', () => {
    topContainer.style.display = 'none';
  });
    bottomContainer.addEventListener('click', () => {
    bottomContainer.style.display = 'none';
  });
    outerContainer.addEventListener('click', () => {
    outerContainer.style.display = 'none';
  });
    shoeContainer.addEventListener('click', () => {
    shoeContainer.style.display = 'none';
  });
    bagContainer.addEventListener('click', () => {
    bagContainer.style.display = 'none';
  });
    accContainer.addEventListener('click', () => {
    accContainer.style.display = 'none';
  });
});

// Gallery Outfit //

  document.addEventListener("DOMContentLoaded", function () {
    const toggleSwitches = document.querySelectorAll('.toggle-switch');

    toggleSwitches.forEach(switchElem => {
      switchElem.addEventListener("click", () => {
        switchElem.classList.toggle('active');
      });
    });
  });