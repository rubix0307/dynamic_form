document.addEventListener('DOMContentLoaded', function() {
    function initializeWebsiteOptionHandlers() {
        const websiteYesRadio = document.querySelector('input[type="radio"][name="shareholder_company_OAE_website"][value="1"]');
        const websiteNoRadio = document.querySelector('input[type="radio"][name="shareholder_company_OAE_website"][value="0"]');
        const websiteInput = document.querySelector('#shareholder-company-OAE-website-detail input[name="shareholder_company_OAE_website"]');

        function updateWebsiteInputRequired() {
            if (websiteYesRadio && websiteYesRadio.checked) {
                websiteInput.setAttribute('required', 'required');
            } else if (websiteInput) {
                websiteInput.removeAttribute('required');
            }
        }

        if (websiteInput) {
            websiteInput.addEventListener('input', function() {
                if (websiteYesRadio) {
                    websiteYesRadio.checked = true;
                }
                updateWebsiteInputRequired();
            });
        }

        if (websiteYesRadio && websiteNoRadio) {
            [websiteYesRadio, websiteNoRadio].forEach(function(radio) {
                radio.addEventListener('change', function() {
                    if (radio.value === '0' && websiteInput) {
                        websiteInput.value = '';
                    }
                    updateWebsiteInputRequired();
                });
            });
        }

        // Initialize required attribute state on load
        updateWebsiteInputRequired();
    }

    // Initialize handlers for existing elements
    initializeWebsiteOptionHandlers();

    // Observe changes to the dynamic form
    const dynamicForm = document.querySelector('.dynamic-form');

    if (dynamicForm) {
        const observer = new MutationObserver(function(mutationsList) {
            for (let mutation of mutationsList) {
                if (mutation.type === 'childList') {
                    initializeWebsiteOptionHandlers();
                }
            }
        });

        observer.observe(dynamicForm, { childList: true, subtree: true });
    }
});
