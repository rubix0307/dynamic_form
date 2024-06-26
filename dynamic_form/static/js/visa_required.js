document.addEventListener("DOMContentLoaded", function() {
    // Функция для отслеживания появления блока
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1 && node.classList.contains('form-group')) {
                    // Проверка, что в блоке есть нужные элементы
                    if (node.querySelector('input[type="radio"][name="visa_required"][value="1"]') &&
                        node.querySelector('input[type="radio"][name="visa_required"][value="0"]') &&
                        node.querySelector('#visa-detail')) {
                        // Блок найден, запускаем отслеживание действий с ним
                        trackVisaFormGroup(node);
                    }
                }
            });
        });
    });

    // Настройки для отслеживания добавления новых элементов
    observer.observe(document.body, { childList: true, subtree: true });

    // Функция для отслеживания действий с блоком
    function trackVisaFormGroup(formGroup) {
        const yesRadio = formGroup.querySelector('input[type="radio"][name="visa_required"][value="1"]');
        const noRadio = formGroup.querySelector('input[type="radio"][name="visa_required"][value="0"]');
        const visaDetail = formGroup.querySelector('#visa-detail');

        if (yesRadio && noRadio && visaDetail) {
            yesRadio.addEventListener('change', function() {
                if (yesRadio.checked) {
                    visaDetail.innerHTML = '';
                    let div = document.createElement('div');
                    div.setAttribute('hx-post', 'get_form/?part=visa_detail');
                    div.setAttribute('hx-trigger', 'load');
                    div.setAttribute('hx-target', '#visa-detail');
                    div.setAttribute('hx-swap', 'innerHTML');

                    document.body.appendChild(div);
                    htmx.process(div);
                }
            });

            noRadio.addEventListener('change', function() {
                if (noRadio.checked) {
                    // Действие при выборе "Нет"
                    visaDetail.innerHTML = '';
                }
            });
        }
    }

    // Проверяем, есть ли уже на странице этот блок при загрузке
    document.querySelectorAll('.form-group').forEach(function(formGroup) {
        if (formGroup.querySelector('input[type="radio"][name="visa_required"][value="1"]') &&
            formGroup.querySelector('input[type="radio"][name="visa_required"][value="0"]') &&
            formGroup.querySelector('#visa-detail')) {
            trackVisaFormGroup(formGroup);
        }
    });
});
