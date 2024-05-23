function checkInputsBlock5(btn) {
    let is_good = true;

    let radio1Answered = checkRadioGroups('data-block5-check-radio1');
    let radio2Answered = checkRadioGroups('data-block5-check-radio2');


    if (!radio1Answered || !radio2Answered) {
        is_good = false;
    }


    if (is_good) {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=visa');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#visa');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        btn.style.display = 'none';
        htmx.process(div);

        formScrollToElement('#visa')
    }
}
