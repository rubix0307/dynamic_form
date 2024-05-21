function checkInputsBlock6(btn) {
    let is_good = true
    let radioAnswered = checkRadioGroups('data-block6-check-radio');

    if (!radioAnswered) {
        is_good = false
    }

    let visaQuotaNumber = document.getElementById('visa-quota-number')
    if (visaQuotaNumber && (!visaQuotaNumber.value || visaQuotaNumber.value < 1)) {
        accentElement(visaQuotaNumber.parentElement, 1000)
        is_good = false
    }
    let visaQuotaNumberToMake = document.getElementById('visa-quota-number-to-make')
    if (visaQuotaNumberToMake && (!visaQuotaNumberToMake.value || visaQuotaNumberToMake.value < 0)) {
        accentElement(visaQuotaNumberToMake.parentElement, 1000)
        is_good = false
    }

    if (visaQuotaNumberToMake && visaQuotaNumber && visaQuotaNumberToMake.value > visaQuotaNumber.value) {
        accentElement(visaQuotaNumberToMake.parentElement, 1000)
        is_good = false
    }


    if (is_good) {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=shareholders');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#shareholders');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        btn.style.display = 'none';
        htmx.process(div);
    }
}