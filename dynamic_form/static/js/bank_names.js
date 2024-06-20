document.addEventListener('DOMContentLoaded', function() {
    function initializeTrackingSearchBankNames() {
        let bankList = document.getElementById('bank-names-list');
        let searchInput = document.getElementById('id_search_bank_name');



        function filterBankList() {
            let searchInput = document.getElementById('id_search_bank_name');
            const searchValue = searchInput.value.toLowerCase();
            let bankList = document.getElementById('bank-names-list');
            const listItems = bankList.querySelectorAll('li');

            listItems.forEach(function(item) {
                const bankName = item.textContent.toLowerCase();
                const checkbox = item.querySelector('input[type="checkbox"]');
                if (searchValue === '' || bankName.includes(searchValue)) {
                    item.classList.remove('hidden');
                } else if (!checkbox.checked) {
                    item.classList.add('hidden');
                }
            });
        }

        function sortBankList() {
            let bankList = document.getElementById('bank-names-list');
            const listItems = Array.from(bankList.querySelectorAll('li'));

            listItems.sort((a, b) => {
                const aChecked = a.querySelector('input[type="checkbox"]').checked;
                const bChecked = b.querySelector('input[type="checkbox"]').checked;

                if (aChecked && !bChecked) {
                    return -1;
                } else if (!aChecked && bChecked) {
                    return 1;
                } else {
                    return a.textContent.trim().localeCompare(b.textContent.trim());
                }
            });

            listItems.forEach(item => bankList.appendChild(item));
        }

        function handleCheckboxChange() {
            sortBankList();
        }

        function handleNewItems(bankList) {
            const newCheckboxes = bankList.querySelectorAll('input[type="checkbox"]:not([data-initialized])');
            newCheckboxes.forEach(function(checkbox) {
                checkbox.addEventListener('change', handleCheckboxChange);
                checkbox.setAttribute('data-initialized', 'true'); // Отметка, что обработчик добавлен
            });
        }

        function trackSearch(searchInput) {
            if (searchInput) {
                searchInput.addEventListener('input', filterBankList);
                document.querySelector('.remove').addEventListener('click', clearInput);
                document.querySelector('.remove').addEventListener('click', filterBankList);
            }
        }
        // Создаем новый экземпляр MutationObserver с функцией обратного вызова
        const observer = new MutationObserver(function(mutationsList) {

            let bankList = document.getElementById('bank-names-list');
            let searchInput = document.getElementById('id_search_bank_name');

            mutationsList.forEach(mutation => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    handleNewItems(bankList);
                    filterBankList(bankList);
                    trackSearch(searchInput);


                }
            });
        });

        const dynamicForm = document.querySelector('.dynamic-form');
        if (dynamicForm) {
            observer.observe(dynamicForm, { childList: true, subtree: true });
        }

        handleNewItems(); // Инициализация для уже существующих элементов
        sortBankList();
    }

    initializeTrackingSearchBankNames();
});

function handleBankSelection(radio) {
    let bankDetailDiv = document.getElementById('bank-name-detail');

    if (radio.value === '1') {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=banks_name_list');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#bank-name-detail');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        htmx.process(div);
    } else {
        bankDetailDiv.innerHTML = '';
    }
}
