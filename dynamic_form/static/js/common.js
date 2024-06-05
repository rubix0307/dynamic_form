
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

function checkInputValueExists(attribute) {
    let is_good = true
    let inputs = document.querySelectorAll(`[${attribute}="1"]`);

    inputs.forEach(element => {
        if (!element.value) {
            accentElement(element, 1000)
            is_good = false;
        }
    });

    return is_good;
}

function clearById(id) {
    let element = document.getElementById(id);
    if (element) {
        element.innerHTML = '';
    } else {
        console.log(`Элемент с id="${id}" не найден.`);
    }
}

function setupDynamicInput(inputElementId, hxPost, hxTarget, hxTrigger) {
    var inputElement = document.getElementById(inputElementId);
    inputElement.setAttribute('hx-target', hxTarget);
    inputElement.setAttribute('hx-trigger', hxTrigger);
    inputElement.setAttribute('hx-post', hxPost.replace('${inputElement.value}', inputElement.value));

    inputElement.addEventListener('input', function() {
        var targetElement = document.querySelector(hxTarget);

        if (inputElement.value.length > 0) {
            inputElement.setAttribute('hx-target', hxTarget);
            inputElement.setAttribute('hx-post', hxPost.replace('${inputElement.value}', inputElement.value));

        } else {
            if (targetElement) {
                targetElement.innerHTML = '';  // Очищаем содержимое цели
            }
            inputElement.removeAttribute('hx-target');
        }
    });
    htmx.process(inputElement);

}
function formScrollToElement(elementSelector) {
    const form = document.querySelector('.dynamic-form');
    const spaceElement= form.querySelector(elementSelector);
    if (spaceElement) {
        setTimeout(() => {
            spaceElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }, 300);

    }
}


function showTab(tabId, scrollTo) {
    // Скрыть все элементы с классом .tab
    let tabs = document.querySelectorAll('.tab');
    tabs.forEach(function(tab) {
        tab.style.display = 'none';
    });

    // Показать элемент с указанным id
    let tabToShow = document.getElementById(tabId);
    if (tabToShow) {
        tabToShow.style.display = 'block';
    } else {
        console.warn(`Element with id "${tabId}" not found.`);
    }


    if (scrollTo) {
        formScrollToElement(scrollTo)
    }
}



