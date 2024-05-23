function checkInputsBlock3(btn) {
    let is_good = true;

    // Проверка radio-инпутов
    const radioElements = document.querySelectorAll('[data-block3-check-radio="1"]');
    radioElements.forEach(element => {
        const radios = element.querySelectorAll('input[type="radio"]');
        let answered = false;

        radios.forEach(radio => {
            if (radio.checked) {
                answered = true;
            }
        });

        if (!answered) {
            is_good = false;
            element.classList.add('empty-input');
            setTimeout(() => {
                element.classList.remove('empty-input');
            }, 1000);
        }
    });

    // Проверка text-инпутов
    const textElements = document.querySelectorAll('[data-block3-check-text="1"]');
    textElements.forEach(element => {
        const texts = element.querySelectorAll('input[type="text"]');

        texts.forEach(text => {
            if (text.value.trim() === '') {
                is_good = false;

                text.classList.add('empty-input');
                setTimeout(() => {
                    text.classList.remove('empty-input');
                }, 1000);
            }
        });

    });

    if (is_good) {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=registration_preferences');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#registration_preferences');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        btn.style.display = 'none';
        htmx.process(div);



        const elementsToHide = document.querySelectorAll('[data-hide-block3="1"]');
        elementsToHide.forEach(element => {
            element.style.display = 'none';
        });
        const elementsToNotActive = document.querySelectorAll('[data-notactive-block3="1"]');
        elementsToNotActive.forEach(element => {
            element.style.pointerEvents = 'none';
        });


        formScrollToElement('#registration_preferences')
    }

    return is_good;
}


