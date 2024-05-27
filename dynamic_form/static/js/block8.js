function listenOffice() {
    // Получаем все радио-кнопки с именем "office"
    var officeRadios = document.querySelectorAll('input[name="office"]');

    function toggleRealOfficeArea() {
        var realOfficeArea = document.getElementById('real_office_area');
        var realOfficeInputArea = document.getElementById('real_office_input_area');

        if (document.getElementById('real_office').checked) {
            realOfficeArea.style.display = 'block';
            // Создаем новый input элемент
            var inputElement = document.createElement('input');
            inputElement.type = 'number';
            inputElement.min = '1';
            inputElement.placeholder = 'м2';
            inputElement.id = 'real_office_input';
            inputElement.name = 'real_office_area';
            inputElement.required = true;
            inputElement.setAttribute('data-office-area-check', '1');

            // Добавляем input элемент в real_office_input_area
            realOfficeInputArea.appendChild(inputElement);
        } else {
            // Удаляем содержимое real_office_input_area
            realOfficeInputArea.innerHTML = '';
            realOfficeArea.style.display = 'none';
        }
    }
    // Добавляем обработчик события на изменение для каждого радио-кнопки
    officeRadios.forEach(function (radio) {
        radio.addEventListener('change', toggleRealOfficeArea);
    });

    // Изначально скрываем блок, если значение "real" не выбрано
    toggleRealOfficeArea();
}

function checkInputsBlock8(btn) {
    let is_good = true;
    let radioAnsweredOffice = checkRadioGroups('data-block8-check-radio-office');
    let radioAnsweredBank = checkRadioGroups('data-block8-check-radio-bank');

    if (!radioAnsweredOffice) {
        is_good = false;
    }
    if (!radioAnsweredBank) {
        is_good = false;
    }


    let realOfficeOption = document.querySelector('input[name="office"][value="real"]');
    if (realOfficeOption.checked) {
        let officeAreaExists = checkInputValueExists('data-office-area-check')

        if (!officeAreaExists) {
            is_good = false;
        }
    }


    let needBankAccount = document.querySelector('input[name="bank_account"][value="1"]');
    if (needBankAccount.checked) {
        let anyElementsForBackRequired = document.querySelectorAll(`[data-need-office-for-bank="1"]`);
        let isChecked = Array.from(anyElementsForBackRequired).some(element => element.checked);

        if (!isChecked) {
            anyElementsForBackRequired.forEach(element => {
                accentElement(element.parentElement, 1000)
            });
            is_good = false;
        }
    }

    if (is_good) {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=customer_data');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#customer_data');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        btn.style.display = 'none';
        htmx.process(div);

        formScrollToElement('#customer_data')
    }


}