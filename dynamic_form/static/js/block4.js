function clearRegistrationPreferencesDetail() {
    var element = document.getElementById('RegistrationPreferencesSelected');
    if (element) {
        element.innerHTML = ''; // Это удалит всё содержимое внутри элемента
    } else {
        console.log('Элемент с id="RegistrationPreferencesSelected" не найден.');
    }
}


function removeEmirate(button) {
    var emiratePlace = button.closest('.secondary-place');
    emiratePlace.remove();
    var dataUrl = emiratePlace.getAttribute('data-url');
    var liElements = document.querySelectorAll('#emirates-list li');
    liElements.forEach(function(li) {
        if (li.getAttribute('hx-get') === dataUrl) {
            li.style.display = '';
        }
    });
}


function checkInputsBlock4(btn) {
    let is_good = true
    let radioAnswered = false;

    const radioElements = document.querySelectorAll('[data-block4-check-radio="1"]');
    radioElements.forEach(element => {
        const radios = element.querySelectorAll('input[type="radio"]');
        radios.forEach(radio => {
            if (radio.checked) {
                radioAnswered = true;
            }
        });
    });

    if (!radioAnswered) {
        is_good = false;

        radioElements.forEach(element => {
            element.classList.add('empty-input');
            setTimeout(() => {
                element.classList.remove('empty-input');
            }, 1000);
        })
    }

    let selectedEmirates = document.getElementById('selected-emirates')
    if (selectedEmirates && document.getElementById('selected-emirates').children.length === 0) {
        let emiratesList= document.getElementById('emirates-list').parentElement;
        emiratesList.classList.add('empty-input');
        setTimeout(() => {
            emiratesList.classList.remove('empty-input');
        }, 1000);
        is_good = false;
    }

    if (is_good) {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=outsource');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#outsource');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        btn.style.display = 'none';
        htmx.process(div);

        formScrollToElement('#outsource')
    }

}