document.addEventListener('DOMContentLoaded', function() {
    function initializeCustomOptionHandlers() {
        const customRadio = document.querySelector('input[type="radio"][value="custom"]');
        const customInput = document.querySelector('input[name="bank_minimal_monthly_custom_balance"]');
        const radioButtons = document.querySelectorAll('input[type="radio"][name="bank_minimal_monthly_balance"]');

        function updateCustomInputRequired() {
            if (customRadio && customRadio.checked) {
                customInput.setAttribute('required', 'required');
            } else if (customInput) {
                customInput.removeAttribute('required');
            }
        }

        if (customInput) {
            customInput.addEventListener('input', function() {
                if (customRadio) {
                    customRadio.checked = true;
                }
                updateCustomInputRequired();
            });
        }

        radioButtons.forEach(function(radio) {
            radio.addEventListener('change', function() {
                if (radio.value !== 'custom' && customInput) {
                    customInput.value = '';
                }
                updateCustomInputRequired();
            });
        });

        // Initialize required attribute state on load
        updateCustomInputRequired();
    }

    // Initialize handlers for existing elements
    initializeCustomOptionHandlers();

    // Observe changes to the dynamic form
    const dynamicForm = document.querySelector('.dynamic-form');

    if (dynamicForm) {
        const observer = new MutationObserver(function(mutationsList) {
            for (let mutation of mutationsList) {
                if (mutation.type === 'childList') {
                    initializeCustomOptionHandlers();
                }
            }
        });

        observer.observe(dynamicForm, { childList: true, subtree: true });
    }
});
