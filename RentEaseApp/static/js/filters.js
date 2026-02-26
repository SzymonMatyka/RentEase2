// Modal functionality for advanced filters
function openFiltersModal() {
    const modal = document.getElementById('filtersModal');
    const form = document.getElementById('filterForm');
    
    if (modal && form) {
        // Sync current form values to modal inputs (for advanced filters that might have values)
        const formInputs = form.querySelectorAll('input, select');
        formInputs.forEach(formInput => {
            const name = formInput.getAttribute('name');
            if (name) {
                const modalInput = modal.querySelector(`[name="${name}"]`);
                if (modalInput && modalInput !== formInput) {
                    if (modalInput.type === 'number' || modalInput.type === 'text') {
                        modalInput.value = formInput.value || '';
                    } else if (modalInput.tagName === 'SELECT' && formInput.tagName === 'SELECT') {
                        modalInput.value = formInput.value || '';
                    }
                }
            }
        });
        
        modal.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

function closeFiltersModal() {
    const modal = document.getElementById('filtersModal');
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

function clearFiltersModal() {
    // Clear all filter inputs in the modal
    const modal = document.getElementById('filtersModal');
    const form = document.getElementById('filterForm');
    
    if (modal) {
        const inputs = modal.querySelectorAll('input, select');
        inputs.forEach(input => {
            if (input.type === 'number' || input.type === 'text') {
                input.value = '';
                // Also clear corresponding form input if it exists
                if (form) {
                    const formInput = form.querySelector(`[name="${input.getAttribute('name')}"]`);
                    if (formInput && formInput !== input) {
                        formInput.value = '';
                    }
                }
            } else if (input.tagName === 'SELECT') {
                input.selectedIndex = 0; // Select "All" option
                // Also clear corresponding form select if it exists
                if (form) {
                    const formSelect = form.querySelector(`select[name="${input.getAttribute('name')}"]`);
                    if (formSelect && formSelect !== input) {
                        formSelect.selectedIndex = 0;
                    }
                }
            }
        });
    }
}

function applyFiltersModal() {
    // Sync modal values to form inputs and submit
    const form = document.getElementById('filterForm');
    const modal = document.getElementById('filtersModal');
    
    if (form && modal) {
        // Get all inputs from the modal
        const modalInputs = modal.querySelectorAll('input, select');
        
        // Update or create form inputs with modal values
        modalInputs.forEach(modalInput => {
            const name = modalInput.getAttribute('name');
            if (name) {
                // Check if input already exists in form
                let formInput = form.querySelector(`[name="${name}"]`);
                
                if (!formInput) {
                    // Create new hidden input if it doesn't exist
                    formInput = document.createElement('input');
                    formInput.type = 'hidden';
                    formInput.name = name;
                    form.appendChild(formInput);
                }
                
                // Update the value
                if (modalInput.type === 'number' || modalInput.type === 'text') {
                    formInput.value = modalInput.value || '';
                } else if (modalInput.tagName === 'SELECT') {
                    if (formInput.tagName === 'SELECT') {
                        formInput.value = modalInput.value || '';
                    } else {
                        formInput.value = modalInput.value || '';
                    }
                }
            }
        });
        
        // Close modal and submit form
        closeFiltersModal();
        // Small delay to allow modal close animation
        setTimeout(() => {
            form.submit();
        }, 200);
    }
}

// Close modal on Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeFiltersModal();
    }
});

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('filtersModal');
    if (modal) {
        const overlay = modal.querySelector('.filters-modal-overlay');
        if (overlay) {
            overlay.addEventListener('click', closeFiltersModal);
        }
    }
});

