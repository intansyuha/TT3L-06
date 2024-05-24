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

document.addEventListener("DOMContentLoaded", function () {
    const saveButton = document.querySelector('.btn-save');
    saveButton.addEventListener('click', () => {
        const selectedOutfit = {
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
    });
});
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

    // const saveButton = document.querySelector('#saveButton');
    // saveButton.addEventListener('click', function () {
    //     alert('Outfit saved!');
    // });
});

document.addEventListener("DOMContentLoaded", function () {
    const saveButton = document.querySelector('#saveButton');

    saveButton.addEventListener('click', () => {
        // Display a custom input prompt
        const outfitName = prompt('Enter the name of your outfit:');
        
        // Check if the user entered a valid outfit name
        if (outfitName !== null && outfitName.trim() !== '') {
            // Proceed to save the outfit with the entered name
            alert(`Outfit "${outfitName}" saved!`);
            // Here you can proceed to save the outfit with the given name
        } else {
            alert('Please enter a valid outfit name.');
        }
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


document.addEventListener('DOMContentLoaded', () => {
  const cardsContainer = document.getElementById('cardsContainer');
  const savedOutfits = JSON.parse(localStorage.getItem('savedOutfits')) || [];

  // Function to create a new outfit card
  function createOutfitCard(outfit) {
    // Create the card container
    const card = document.createElement('a');
    card.href = '#';
    card.className = 'card';

    // Create the image element
    const img = document.createElement('img');
    img.src = outfit.top; // Use the top image from the saved outfit
    img.alt = '';

    // Create the card body
    const cardBody = document.createElement('div');
    cardBody.className = 'card_body';

    // Create the card title
    const cardTitle = document.createElement('h6');
    cardTitle.className = 'card_title';
    cardTitle.textContent = `Saved Outfit ${savedOutfits.indexOf(outfit) + 1}`;

    // Create the card options container
    const cardOptions = document.createElement('div');
    cardOptions.className = 'card_options';

    // Create the toggle switch
    const toggleSwitch = document.createElement('div');
    toggleSwitch.className = 'toggle-switch';
    const switchSpan = document.createElement('span');
    switchSpan.className = 'switch';
    toggleSwitch.appendChild(switchSpan);

    // Create the delete icon
    const deleteDiv = document.createElement('div');
    deleteDiv.className = 'delete';
    const deleteIcon = document.createElement('i');
    deleteIcon.className = 'bx bx-trash bx-sm';
    deleteDiv.appendChild(deleteIcon);

    // Append the toggle switch and delete icon to card options
    cardOptions.appendChild(toggleSwitch);
    cardOptions.appendChild(deleteDiv);

    // Append the title and options to the card body
    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardOptions);

    // Append the image and card body to the card container
    card.appendChild(img);
    card.appendChild(cardBody);

    // Append the card to the cards container
    cardsContainer.appendChild(card);
  }


  // Display saved outfits
  savedOutfits.forEach(outfit => {
    createOutfitCard(outfit);
  });

  // Add event listener for the delete functionality
  cardsContainer.addEventListener('click', function(event) {
    if (event.target.classList.contains('bx-trash')) {
      const card = event.target.closest('.card');
      card.remove();

      // Remove outfit from savedOutfits array
      const outfitIndex = savedOutfits.findIndex(outfit => outfit.imageUrl === card.querySelector('img').src);
      if (outfitIndex !== -1) {
        savedOutfits.splice(outfitIndex, 1);
        // Update local storage
        localStorage.setItem('savedOutfits', JSON.stringify(savedOutfits));
      }
    }
  });

  // Add event listener for the toggle switch functionality
  cardsContainer.addEventListener('click', function(event) {
    if (event.target.classList.contains('switch')) {
      event.target.closest('.toggle-switch').classList.toggle('active');
    }
  });
});
