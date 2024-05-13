const tabs = document.querySelectorAll('[data-tab-target]')
const tabContents = document.querySelectorAll('[data-tab-content]')
const categorySelect = document.getElementById("categoryselect")
const categoryInput = document.getElementById("categoryinput")

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

categorySelect.addEventListener("change", () => {
    categoryInput.value = categorySelect.value
})
