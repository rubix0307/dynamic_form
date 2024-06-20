document.addEventListener('DOMContentLoaded', function() {
    function initializePreviousBanksHandlers() {
        const noPreviousBanksRadio = document.querySelector('input[type="radio"][name="previous_banks"][value="0"]');
        const hasPreviousBanksRadio = document.querySelector('input[type="radio"][name="previous_banks"][value="1"]');
        const previousBanksTextarea = document.querySelector('textarea[name="previous_banks_data"]');

        function updateTextareaRequired() {
            if (hasPreviousBanksRadio && hasPreviousBanksRadio.checked) {
                previousBanksTextarea.setAttribute('required', 'required');
            } else if (previousBanksTextarea) {
                previousBanksTextarea.removeAttribute('required');
            }
        }

        if (previousBanksTextarea) {
            previousBanksTextarea.addEventListener('input', function() {
                if (hasPreviousBanksRadio) {
                    hasPreviousBanksRadio.checked = true;
                }
                updateTextareaRequired();
            });
        }

        if (noPreviousBanksRadio && hasPreviousBanksRadio) {
            [noPreviousBanksRadio, hasPreviousBanksRadio].forEach(function(radio) {
                radio.addEventListener('change', function() {
                    if (radio.value === '0' && previousBanksTextarea) {
                        previousBanksTextarea.value = '';
                    }
                    updateTextareaRequired();
                });
            });
        }

        // Initialize required attribute state on load
        updateTextareaRequired();
    }

    // Initialize handlers for existing elements
    initializePreviousBanksHandlers();

    // Observe changes to the dynamic form
    const dynamicForm = document.querySelector('.dynamic-form');

    if (dynamicForm) {
        const observer = new MutationObserver(function(mutationsList) {
            for (let mutation of mutationsList) {
                if (mutation.type === 'childList') {
                    initializePreviousBanksHandlers();
                }
            }
        });

        observer.observe(dynamicForm, { childList: true, subtree: true });
    }
});
