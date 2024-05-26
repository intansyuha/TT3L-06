// Accordion functionality
const labels = document.querySelectorAll('.accordion-row label');

labels.forEach(label => {
  const accordionContent = label.nextElementSibling;
  accordionContent.style.display = 'none';
});

labels.forEach(label => {
    label.addEventListener('click', () => {
        const accordionContent = label.nextElementSibling;
        const chevron = label.querySelector('i');

        accordionContent.style.display = accordionContent.style.display === 'flex' ? 'none' : 'flex';

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

// Outfit selection and display functionality
document.addEventListener("DOMContentLoaded", function () {
  const topSmallBoxes = document.querySelectorAll('#tops-accordion .sb-1 .sb');
  const topContainer = document.querySelector('.top-container');
  const topContainerImg = document.querySelector('.top-container img');

  const bottomSmallBoxes = document.querySelectorAll('#bottoms-accordion .sb'); 
  const bottomContainer = document.querySelector('.bottom-container');
  const bottomContainerImg = document.querySelector('.bottom-container img');

  const outerSmallBoxes = document.querySelectorAll('#outerwear-accordion .sb');
  const outerContainer = document.querySelector('.outerwear-container');
  const outerContainerImg = document.querySelector('.outerwear-container img');

  const shoeSmallBoxes = document.querySelectorAll('#shoes-accordion .sb');
  const shoeContainer = document.querySelector('.shoes-container');
  const shoeContainerImg = document.querySelector('.shoes-container img');

  const bagSmallBoxes = document.querySelectorAll('#bags-accordion .sb');
  const bagContainer = document.querySelector('.bags-container');
  const bagContainerImg = document.querySelector('.bags-container img');

  const accSmallBoxes = document.querySelectorAll('#accessories-accordion .sb');
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

// Save outfit functionality with name prompt
document.addEventListener("DOMContentLoaded", function () {
    const saveButton = document.querySelector('.btn-save');
    saveButton.addEventListener('click', () => {
        let outfitName = prompt('Enter the name of your outfit:');

        // Keep prompting until a valid name is entered
        while (outfitName !== null && outfitName.trim() === '') {
            alert('Please enter a valid outfit name.');
            outfitName = prompt('Enter the name of your outfit:');
        }

        if (outfitName !== null) { // Check if the user provided a name
            const selectedOutfit = {
                name: outfitName.trim(),
                top: document.querySelector('.top-container img').src,
                bottom: document.querySelector('.bottom-container img').src,
                outerwear: document.querySelector('.outerwear-container img').src,
                shoes: document.querySelector('.shoes-container img').src,
                bags: document.querySelector('.bags-container img').src,
                accessories: document.querySelector('.accessories-container img').src
            };

            let savedOutfits = JSON.parse(localStorage.getItem('savedOutfits')) || [];
            savedOutfits.push(selectedOutfit);
            localStorage.setItem('savedOutfits', JSON.stringify(savedOutfits));
            alert(`Outfit "${outfitName}" saved!`);
        }
    });
});


// Sidebar and overlay functionality
document.addEventListener("DOMContentLoaded", function () {
    const menuIcon = document.querySelectorAll('.menu-icon');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('#overlay');
    
    menuIcon.forEach(icon => {
        icon.addEventListener('click', function () {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('open');
        });
    });
    
    overlay.addEventListener('click', function () {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
    });
    
    const accordionLabels = document.querySelectorAll('.accordion-row label');
    accordionLabels.forEach(label => {
        label.addEventListener('click', function () {
            this.nextElementSibling.classList.toggle('hidden');
        });
    });
});

// Gallery functionality
document.addEventListener("DOMContentLoaded", function () {
    const toggleSwitches = document.querySelectorAll('.toggle-switch');

    toggleSwitches.forEach(switchElem => {
        switchElem.addEventListener("click", () => {
            switchElem.classList.toggle('active');
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const cardsContainer = document.getElementById('cardsContainer');
    const savedOutfits = JSON.parse(localStorage.getItem('savedOutfits')) || [];

    function createOutfitCard(outfit) {
        const card = document.createElement('a');
        card.href = '#';
        card.className = 'card';

        const img = document.createElement('img');
        img.src = outfit.top;
        img.alt = '';

        const cardBody = document.createElement('div');
        cardBody.className = 'card_body';

        const cardTitle = document.createElement('h6');
        cardTitle.className = 'card_title';
        cardTitle.textContent = outfit.name;

        const cardOptions = document.createElement('div');
        cardOptions.className = 'card_options';

        const toggleSwitch = document.createElement('div');
        toggleSwitch.className = 'toggle-switch';
        const switchSpan = document.createElement('span');
        switchSpan.className = 'switch';
        toggleSwitch.appendChild(switchSpan);

        const deleteDiv = document.createElement('div');
        deleteDiv.className = 'delete';
        const deleteIcon = document.createElement('i');
        deleteIcon.className = 'bx bx-trash bx-sm';
        deleteDiv.appendChild(deleteIcon);

        cardOptions.appendChild(toggleSwitch);
        cardOptions.appendChild(deleteDiv);

        cardBody.appendChild(cardTitle);
        cardBody.appendChild(cardOptions);

        card.appendChild(img);
        card.appendChild(cardBody);

        cardsContainer.appendChild(card);
    }

    savedOutfits.forEach(outfit => {
        createOutfitCard(outfit);
    });

    cardsContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('bx-trash')) {
            const card = event.target.closest('.card');
            const imageUrl = card.querySelector('img').src;
            const outfitIndex = savedOutfits.findIndex(outfit => outfit.top === imageUrl);
            if (outfitIndex !== -1) {
                savedOutfits.splice(outfitIndex, 1);
                localStorage.setItem('savedOutfits', JSON.stringify(savedOutfits));
                card.remove();
                alert('Outfit has been deleted!');
            }
        }
    });

    cardsContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('switch')) {
            event.target.closest('.toggle-switch').classList.toggle('active');
        }
    });
});
