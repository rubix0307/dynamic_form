document.addEventListener("DOMContentLoaded", function() {
    // Функция для отслеживания появления блока
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1 && node.classList.contains('form-group')) {
                    // Проверка, что в блоке есть нужные элементы
                    if (node.querySelector('input[type="radio"][name="is_home_company_website"][value="1"]') &&
                        node.querySelector('input[type="radio"][name="is_home_company_website"][value="0"]') &&
                        node.querySelector('input[type="url"][name="is_home_company_website_input"]')) {
                        // Блок найден, запускаем отслеживание действий с ним
                        trackFormGroup(node);
                    }
                }
            });
        });
    });

    // Настройки для отслеживания добавления новых элементов
    observer.observe(document.body, { childList: true, subtree: true });

    // Функция для отслеживания действий с блоком
    function trackFormGroup(formGroup) {
        const yesRadio = formGroup.querySelector('input[type="radio"][name="is_home_company_website"][value="1"]');
        const noRadio = formGroup.querySelector('input[type="radio"][name="is_home_company_website"][value="0"]');
        const websiteInput = formGroup.querySelector('input[type="url"][name="is_home_company_website_input"]');

        if (yesRadio && noRadio && websiteInput) {
            yesRadio.addEventListener('change', function() {
                if (yesRadio.checked) {
                    websiteInput.setAttribute('required', '');
                }
            });

            noRadio.addEventListener('change', function() {
                if (noRadio.checked) {
                    websiteInput.removeAttribute('required');
                    websiteInput.value = '';
                }
            });
        }
    }

    // Проверяем, есть ли уже на странице этот блок при загрузке
    document.querySelectorAll('.form-group').forEach(function(formGroup) {
        if (formGroup.querySelector('input[type="radio"][name="is_home_company_website"][value="1"]') &&
            formGroup.querySelector('input[type="radio"][name="is_home_company_website"][value="0"]') &&
            formGroup.querySelector('input[type="url"][name="is_home_company_website_input"]')) {
            trackFormGroup(formGroup);
        }
    });
});
