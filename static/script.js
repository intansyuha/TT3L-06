const tabs = document.querySelectorAll('[data-tab-target]');
const tabContents = document.querySelectorAll('[data-tab-content]');

// Function to activate the tab based on the target
function activateTab(targetId) {
    const target = document.querySelector(targetId);
    tabContents.forEach(tabContent => {
        tabContent.classList.remove('active');
    });
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    const activeTab = document.querySelector(`[data-tab-target="${targetId}"]`);
    if (activeTab) {
        activeTab.classList.add('active');
    }
    if (target) {
        target.classList.add('active');
    }
}

// Event listeners for tab clicks
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const target = tab.dataset.tabTarget;
        activateTab(target);
    });
});

// Automatically open the tab corresponding to the selected category
document.addEventListener('DOMContentLoaded', () => {
    if (typeof category !== 'undefined' && category) {
        activateTab(`#${category.toLowerCase()}`);
    }
});
