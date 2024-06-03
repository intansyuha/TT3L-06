
///// category tab //////

const tabs = document.querySelectorAll('.tab')
const tabContents = document.querySelectorAll('[data-tab-content]')

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
