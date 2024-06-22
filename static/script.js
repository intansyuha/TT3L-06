document.addEventListener('DOMContentLoaded', () => {
    // Sidebar outfitcreator, outfitgallery, index, imgwindow functionality
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
});

// Wardrobe Category //
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = document.querySelector(tab.dataset.tabTarget);

            tabContents.forEach(tabContent => {
                tabContent.classList.remove('active');
            });

            tabs.forEach(tab => {
                tab.classList.remove('active');
            });

            tab.classList.add('active');
            target.classList.add('active');
        });
    });

    const imageContainer = document.getElementById('imageContainer');

    if (imageContainer) {
        imageContainer.addEventListener('click', function(event) {
            if (event.target.classList.contains('deleteButton')) {
                event.stopPropagation();
                const imageDiv = event.target.parentNode;
                const fileUrl = imageDiv.querySelector('img').src;
                const filename = decodeURIComponent(fileUrl.split('/').pop()); // Ensure URL encoding is handled

                const confirmation = confirm('Are you sure you want to delete this image?');
                if (confirmation) {
                    deleteImage(filename, imageDiv);
                }
            }
        });
    } else {
        console.error('Image container not found');
    }

    function deleteImage(filename, imageDiv) {
        fetch(`/delete_image/${filename}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Failed to delete image');
        })
        .then(data => {
            if (data.message) {
                alert('Image deleted successfully!');
                imageDiv.remove();
            } else {
                alert('Failed to delete image.');
            }
        })
        .catch(error => {
            console.error('Error deleting image:', error);
            alert('Error deleting the image. Please try again.');
        });
    }
});

//OUTFIT CREATOR//
document.addEventListener('DOMContentLoaded', () => {
    // Accordion functionality
    const labels = document.querySelectorAll('.accordion-row label');
    labels.forEach(label => {
        const accordionContent = label.nextElementSibling;
        accordionContent.style.display = 'none';

        label.addEventListener('click', () => {
            const chevron = label.querySelector('i');
            accordionContent.style.display = accordionContent.style.display === 'flex' ? 'none' : 'flex';
            chevron.classList.toggle('bx-chevron-right');
            chevron.classList.toggle('bx-chevron-down');
        });
    });

    const navBar = document.querySelector("nav");
    const menuBtns = document.querySelectorAll(".menu-icon");
    const overlay = document.querySelector(".overlay");

    menuBtns.forEach(menuBtn => {
        menuBtn.addEventListener("click", () => {
            navBar.classList.toggle("nav");
            navBar.classList.toggle("open");
        });
    });

    overlay.addEventListener("click", () => {
        navBar.classList.remove("nav");
        navBar.classList.remove("open");
    });

    // Outfit gallery functionality
    const cardsContainer = document.getElementById('cardsContainer');

    if (cardsContainer) {
        function fetchOutfits() {
            fetch('/get_outfit')
                .then(response => response.json())
                .then(outfits => {
                    console.log('Fetched outfits:', outfits);  // Log fetched outfits
                    outfits.forEach(outfit => {
                        createOutfitCard(outfit);
                    });
                })
                .catch(error => console.error('Error retrieving outfits:', error));
        }

        function createOutfitCard(outfit) {
            if (!outfit.id) {
                console.error('Outfit ID is missing:', outfit);
                return;
            }

            const card = document.createElement('div');
            card.className = 'Card';
            card.id = `outfit-${outfit.id}`;

            const img = document.createElement('img');
            img.src = outfit.top;
            img.alt = outfit.name;

            const cardBody = document.createElement('div');
            cardBody.className = 'Card_body';

            const cardTitle = document.createElement('h6');
            cardTitle.className = 'Card_title';
            cardTitle.textContent = outfit.name;

            const cardOptions = document.createElement('div');
            cardOptions.className = 'Card_options';

            // upload
            const uploadDiv = document.createElement('div');
            uploadDiv.className = 'upload';
            uploadDiv.setAttribute('data-id', outfit.id);

            const uploadIcon = document.createElement('i');
            uploadIcon.className = 'bx bx-cloud-upload bx-sm';
            uploadDiv.appendChild(uploadIcon);

            uploadDiv.addEventListener('click', async function(event) {
                event.stopPropagation(); // Prevents the card click event from firing

                const outfitId = this.getAttribute('data-id');
                const outfitName = outfit.name;
                const confirmation = confirm(`Are you sure you want to publish the outfit "${outfitName}"?`);

                if (confirmation) {
                    let caption = prompt("Enter a caption for your outfit (not more than 100 words):");

                    while (caption && caption.split(/\s+/).length > 100) {
                        alert('Caption exceeds 100 words. Please enter a shorter caption.');
                        caption = prompt("Enter a caption for your outfit (not more than 100 words):");
                    }

                    try {
                        const response = await fetch(`/upload_outfit/${outfitId}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ caption })
                        });

                        const data = await response.json(); // Parsing the JSON response
                        console.log(data); // Log the response to see what's actually returned

                        if (response.ok && data.message === "Outfit published successfully") {
                            alert('Outfit published successfully!');
                        } else {
                            throw new Error(`Failed to publish the outfit: ${data.message}`);
                        }
                    } catch (error) {
                        console.error('Error publishing outfit:', error);
                        alert('Error publishing the outfit. Please try again.');
                    }
                }
            });


            //delete

            const deleteDiv = document.createElement('div');
            deleteDiv.className = 'delete';
            deleteDiv.setAttribute('data-id', outfit.id);
            const deleteIcon = document.createElement('i');
            deleteIcon.className = 'bx bx-trash bx-sm';
            deleteDiv.appendChild(deleteIcon);

            deleteDiv.addEventListener('click', function (event) {
                event.stopPropagation(); // Prevents the card click event from firing
                const outfitId = this.getAttribute('data-id');
                console.log(`Deleting outfit with ID: ${outfitId}`);  // Logging the outfit ID
                const cardElement = this.closest('.Card');
                const confirmation = confirm(`Are you sure you want to delete the outfit "${outfit.name}"?`);

                if (confirmation) {
                    deleteOutfit(outfitId, cardElement);
                }
            });

            cardOptions.appendChild(uploadDiv);
            cardOptions.appendChild(deleteDiv);
            cardBody.appendChild(cardTitle);
            cardBody.appendChild(cardOptions);
            card.appendChild(img);
            card.appendChild(cardBody);

            card.addEventListener('click', () => {
                const queryParams = new URLSearchParams({
                    top: outfit.top,
                    bottom: outfit.bottom,
                    outerwear: outfit.outerwear,
                    shoes: outfit.shoes,
                    bags: outfit.bags,
                    accessories: outfit.accessories,
                }).toString();
                window.location.href = `/outfitcreator.html?${queryParams}`;
            });

            cardsContainer.appendChild(card);
        }

        //delete func

        function deleteOutfit(outfitId, cardElement) {
            fetch(`/delete_outfit/${outfitId}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (response.ok) {
                    alert('Outfit deleted successfully!');
                    cardElement.remove();
                } else {
                    return response.json().then(data => {
                        console.error('Failed to delete the outfit:', data.message);
                        alert('Failed to delete the outfit.');
                    });
                }
            })
            .catch(error => {
                console.error('Error deleting outfit:', error);
                alert('Error deleting the outfit. Please try again.');
            });
        }

        fetchOutfits();
    } else {
        console.error('Cards container not found');
    }
});

//OUTFIT GALLERY//
document.addEventListener('DOMContentLoaded', () => {
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
                    top: document.querySelector('.top-container img')?.src || '',
                    bottom: document.querySelector('.bottom-container img')?.src || '',
                    outerwear: document.querySelector('.outerwear-container img')?.src || '',
                    shoes: document.querySelector('.shoes-container img')?.src || '',
                    bags: document.querySelector('.bags-container img')?.src || '',
                    accessories: document.querySelector('.accessories-container img')?.src || ''
                };

                console.log('Saving outfit:', selectedOutfit); // Debugging log

                fetch('/save_outfit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(selectedOutfit)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(`Outfit "${outfitName}" saved!`);
                    } else {
                        alert('Failed to save outfit.');
                    }
                })
                .catch(error => console.error('Error saving outfit:', error));
            }
        });
    }
});


/// EDIT CLOTHES IN OUTFIT GALLERY ///
function saveEditedOutfit() {
    const editedOutfit = {
        id: outfitId, // You need to populate this with the ID of the outfit being edited
        name: document.getElementById('editedOutfitName').value,
        top: document.getElementById('editedTopURL').value,
        bottom: document.getElementById('editedBottomURL').value,
        outerwear: document.getElementById('editedOuterwearURL').value,
        shoes: document.getElementById('editedShoesURL').value,
        bags: document.getElementById('editedBagsURL').value,
        accessories: document.getElementById('editedAccessoriesURL').value
    };

    fetch('/update_outfit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editedOutfit)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Failed to update outfit');
    })
    .then(data => {
        if (data.message) {
            alert('Outfit updated successfully!');
        } else {
            alert('Failed to update outfit.');
        }
    })
    .catch(error => {
        console.error('Error updating outfit:', error);
        alert('Error updating outfit. Please try again.');
    });
}







//LOGIN//

document.addEventListener('DOMContentLoaded', () => {
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

    const menuItems = document.querySelectorAll('.menu-item');

    // Remove active class from all menu items
    const changeActiveItem = () => {
        menuItems.forEach(item => {
            item.classList.remove('active');
        });
    }
});