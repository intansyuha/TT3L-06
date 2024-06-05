const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('[data-tab-content]');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const target = document.querySelector(tab.dataset.tabTarget)
        tabContents.forEach(tabContent => { 
            tabContent.classList.remove('active')
        })
        tabs.forEach(tab => { 
            tab.classList.remove('active')
        })
        tab.classList.add('active')
        target.classList.add('active')
    })
})

///// delete button //////
document.addEventListener('DOMContentLoaded', function() {
  const imageContainer = document.getElementById('imageContainer');

  if (imageContainer) {
    imageContainer.addEventListener('click', function(event) {
      if (event.target.classList.contains('deleteButton')) {
        console.log('Delete button clicked');
        const imageDiv = event.target.parentNode;
        console.log('Image div:', imageDiv);
        imageDiv.parentNode.removeChild(imageDiv);
      }
    });
  } else {
    console.error('Image container not found');
  }
});

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

document.addEventListener("DOMContentLoaded", function () {
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

    // Outfit selection and display functionality
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

    if (topContainer) {
        topContainer.addEventListener('click', () => {
            topContainer.style.display = 'none';
        });
    }

    if (bottomContainer) {
        bottomContainer.addEventListener('click', () => {
            bottomContainer.style.display = 'none';
        });
    }

    if (outerContainer) {
        outerContainer.addEventListener('click', () => {
            outerContainer.style.display = 'none';
        });
    }

    if (shoeContainer) {
        shoeContainer.addEventListener('click', () => {
            shoeContainer.style.display = 'none';
        });
    }

    if (bagContainer) {
        bagContainer.addEventListener('click', () => {
            bagContainer.style.display = 'none';
        });
    }

    if (accContainer) {
        accContainer.addEventListener('click', () => {
            accContainer.style.display = 'none';
        });
    }

    // Save outfit button
    const saveButton = document.getElementById('saveButton');
    if (saveButton) {
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

                fetch('/save_outfit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(selectedOutfit)
                })
                .then(response => response.json())
                .then(data => alert(`Outfit "${outfitName}" saved!`))
                .catch(error => console.error('Error saving outfit:', error));
            }
        });
    }

    // Gallery functionality
    const cardsContainer = document.getElementById('cardsContainer');

    fetch('/get_outfit')
        .then(response => response.json())
        .then(outfits => {
            console.log('Fetched outfits:', outfits); // Debugging log
            outfits.forEach(outfit => {
                createOutfitCard(outfit);
            });
        })
        .catch(error => console.error('Error retrieving outfits:', error));

    if (cardsContainer) {
        cardsContainer.addEventListener('click', function (event) {
            if (event.target.classList.contains('switch')) {
              event.target.closest('.toggle-switch').classList.toggle('active');
              
            } else if (event.target.classList.contains('bx-trash')) {
                const card = event.target.closest('.Card');
                const imageUrl = card.querySelector('img').src;
                const outfitIndex = savedOutfits.findIndex(outfit => outfit.top === imageUrl);

                if (outfitIndex !== -1) {
                    const outfitName = card.querySelector('.Card_title').textContent;
                    const confirmation = confirm(`Are you sure you want to delete the outfit "${outfitName}"?`);

                    if (confirmation) {
                        savedOutfits.splice(outfitIndex, 1);
                        localStorage.setItem('savedOutfits', JSON.stringify(savedOutfits));
                        card.remove();
                        alert(`Outfit "${outfitName}" has been deleted!`);
                    }
                }
            }
        });
    }

    // Sidebar functionality
    const menuIcon = document.querySelectorAll('.menu-icon');
    const sidebar = document.querySelector('.side-bar');
    const overlaySidebar = document.querySelector('#overlay');
    
    menuIcon.forEach(icon => {
        icon.addEventListener('click', function () {
            sidebar.classList.toggle('open');
            overlaySidebar.classList.toggle('open');
        });
    });

    overlaySidebar.addEventListener('click', function () {
        sidebar.classList.remove('open');
        overlaySidebar.classList.remove('open');
    });

    const accordionLabels = document.querySelectorAll('.accordion-row label');
    accordionLabels.forEach(label => {
        label.addEventListener('click', function () {
            this.nextElementSibling.classList.toggle('hidden');
        });
    });

    // Toggle password visibility
    const showPasswordCheckbox = document.getElementById("showPassword");
    if (showPasswordCheckbox) {
        showPasswordCheckbox.addEventListener('change', togglePassword);
    }

    function togglePassword() {
        const passwordField = document.getElementById("new_password");
        if (showPasswordCheckbox.checked) {
            passwordField.type = "text";
        } else {
            passwordField.type = "password";
        }
    }

    // Profile picture upload
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(event.target);
            const response = await fetch('/update_profile', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                alert('Profile updated successfully!');
                // Optionally, update the UI with the new data
            } else {
                alert('Failed to update profile.');
            }
        });
    }

    const menuItems = document.querySelectorAll('.menu-item');
    const messagesNotification = document.querySelector('#messages-notifications');
    const messages = document.querySelector('.messages');
    const message = messages.querySelectorAll('.message');
    const messageSearch = document.querySelector('#message-search');

    // Remove active class from all menu items
    const changeActiveItem = () => {
        menuItems.forEach(item => {
            item.classList.remove('active');
        });
    }

    // Image upload preview
    function loadImage(event) {
        const output = document.getElementById('profile-picture-preview');
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function () {
            URL.revokeObjectURL(output.src) // free memory
        }
    }
  // Create Outfit Card
    function createOutfitCard(outfit) {
          const card = document.createElement('a');
          card.href = '#';
          card.className = 'Card';
      
          const img = document.createElement('img');
          img.src = outfit.top;
          img.alt = '';
      
          const cardBody = document.createElement('div');
          cardBody.className = 'Card_body';
      
          const cardTitle = document.createElement('h6');
          cardTitle.className = 'Card_title';
          cardTitle.textContent = outfit.name;
      
          const cardOptions = document.createElement('div');
          cardOptions.className = 'Card_options';
      
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
      
            deleteDiv.addEventListener('click', () => {
              const confirmation = confirm(`Are you sure you want to delete the outfit "${outfit.name}"?`);
              if (confirmation) {
                  deleteOutfit(outfit.id, card);
              }
          });
      
          cardOptions.appendChild(toggleSwitch);
          cardOptions.appendChild(deleteDiv);
      
          cardBody.appendChild(cardTitle);
          cardBody.appendChild(cardOptions);
      
          card.appendChild(img);
          card.appendChild(cardBody);
      
          const cardsContainer = document.getElementById('cardsContainer');
          console.log('Appending card to container:', card); // Debugging log
          cardsContainer.appendChild(card);
      }
      
      
    function deleteOutfit(outfitId, cardElement) {
          fetch(`/delete_outfit/${outfitId}`, {
              method: 'DELETE'
          })
          .then(response => {
              if (response.ok) {
                  alert('Outfit deleted successfully!');
                  cardElement.remove(); // Remove the card from the DOM
              } else {
                  alert('Failed to delete the outfit.');
              }
          })
          .catch(error => {
              console.error('Error deleting outfit:', error);
              alert('Error deleting the outfit. Please try again.');
          });
      }
});
