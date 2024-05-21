function checkInputsBlock5(btn) {
    let is_good = true;

    function checkRadioGroups(attribute) {
        let radioAnswered = false;
        let radioElements = document.querySelectorAll(`[${attribute}="1"]`);

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
            });
        }

        return radioAnswered;
    }

    let radio1Answered = checkRadioGroups('data-block5-check-radio1');
    let radio2Answered = checkRadioGroups('data-block5-check-radio2');

    if (is_good) {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=visa');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#visa');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        btn.style.display = 'none';
        htmx.process(div);
    }
}
