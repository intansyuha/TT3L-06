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
    accordionContent.style.display = accordionContent.style.display === 'flex'? 'none' : 'flex';

    // Toggle the chevron icon
    chevron.classList.toggle('bx-chevron-right');
    chevron.classList.toggle('bx-chevron-down');
  });
});