// Gestion de Stock - Les Martial de Informatique
// JavaScript for enhanced functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and interactive elements
    initializeTooltips();
    initializeSearch();
    initializeFilters();
    initializeForms();
});

// Tooltip functionality
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const element = event.target;
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = element.getAttribute('title');
    tooltip.style.cssText = `
        position: absolute;
        background: #1e293b;
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        z-index: 1000;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.2s;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    setTimeout(() => tooltip.style.opacity = '1', 10);
    
    element._tooltip = tooltip;
    element.removeAttribute('title');
}

function hideTooltip(event) {
    const element = event.target;
    if (element._tooltip) {
        element._tooltip.remove();
        delete element._tooltip;
    }
}

// Enhanced search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    }
}

function performSearch(searchTerm) {
    const rows = document.querySelectorAll('#materialsTable tbody tr');
    const term = searchTerm.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const isVisible = text.includes(term);
        row.style.display = isVisible ? '' : 'none';
        
        if (isVisible && term) {
            highlightSearchTerm(row, term);
        } else {
            removeHighlight(row);
        }
    });
    
    updateSearchResults(searchTerm);
}

function highlightSearchTerm(row, term) {
    const cells = row.querySelectorAll('td');
    cells.forEach(cell => {
        const text = cell.textContent;
        const regex = new RegExp(`(${term})`, 'gi');
        const highlightedText = text.replace(regex, '<mark>$1</mark>');
        if (highlightedText !== text) {
            cell.innerHTML = highlightedText;
        }
    });
}

function removeHighlight(row) {
    const marks = row.querySelectorAll('mark');
    marks.forEach(mark => {
        mark.outerHTML = mark.innerHTML;
    });
}

function updateSearchResults(searchTerm) {
    const visibleRows = document.querySelectorAll('#materialsTable tbody tr[style=""]');
    const totalRows = document.querySelectorAll('#materialsTable tbody tr').length;
    
    // You could add a results counter here
    console.log(`Found ${visibleRows.length} of ${totalRows} materials`);
}

// Filter functionality
function initializeFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const stockFilter = document.getElementById('stockFilter');
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', applyFilters);
    }
    if (stockFilter) {
        stockFilter.addEventListener('change', applyFilters);
    }
}

function applyFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const stockFilter = document.getElementById('stockFilter');
    const rows = document.querySelectorAll('#materialsTable tbody tr');
    
    const selectedCategory = categoryFilter ? categoryFilter.value : '';
    const selectedStock = stockFilter ? stockFilter.value : '';
    
    rows.forEach(row => {
        const category = row.dataset.category;
        const stock = row.dataset.stock;
        
        let showRow = true;
        
        if (selectedCategory && category !== selectedCategory) {
            showRow = false;
        }
        
        if (selectedStock && stock !== selectedStock) {
            showRow = false;
        }
        
        row.style.display = showRow ? '' : 'none';
    });
    
    updateFilterResults();
}

function updateFilterResults() {
    const visibleRows = document.querySelectorAll('#materialsTable tbody tr[style=""]');
    console.log(`Filtered results: ${visibleRows.length} materials`);
}

// Form enhancements
function initializeForms() {
    // Auto-save form data
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const formId = form.id || 'form_' + Math.random().toString(36).substr(2, 9);
        form.id = formId;
        
        // Load saved data
        loadFormData(formId);
        
        // Save data on input
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', () => saveFormData(formId));
        });
    });
    
    // Form validation
    const materialForms = document.querySelectorAll('.material-form');
    materialForms.forEach(form => {
        form.addEventListener('submit', validateMaterialForm);
    });
}

function saveFormData(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    localStorage.setItem('form_' + formId, JSON.stringify(data));
}

function loadFormData(formId) {
    const savedData = localStorage.getItem('form_' + formId);
    if (savedData) {
        const data = JSON.parse(savedData);
        const form = document.getElementById(formId);
        
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
            }
        });
    }
}

function validateMaterialForm(event) {
    const form = event.target;
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#ef4444';
            isValid = false;
        } else {
            field.style.borderColor = '';
        }
    });
    
    if (!isValid) {
        event.preventDefault();
        showNotification('Veuillez remplir tous les champs obligatoires', 'error');
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        min-width: 300px;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getNotificationColor(type) {
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#06b6d4'
    };
    return colors[type] || '#06b6d4';
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    }
    
    mark {
        background-color: #fef3c7;
        padding: 0.1rem 0.2rem;
        border-radius: 0.2rem;
    }
`;
document.head.appendChild(style);

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Export functions for global use
window.showNotification = showNotification;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
