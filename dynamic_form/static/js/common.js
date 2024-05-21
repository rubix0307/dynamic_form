
function accentElement(element, time=1000) {
    element.classList.add('empty-input');
    setTimeout(() => {
        element.classList.remove('empty-input');
    }, time);
}


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
        radioElements.forEach(element => {
            accentElement(element, 1000)
        });
    }

    return radioAnswered;
}

function clearById(id) {
    let element = document.getElementById(id);
    if (element) {
        element.innerHTML = '';
    } else {
        console.log(`Элемент с id="${id}" не найден.`);
    }
}