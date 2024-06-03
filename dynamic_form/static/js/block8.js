

function checkInputsBlock8(btn) {
    let is_good = true;

    if (is_good) {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=shareholders');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#shareholders');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        btn.style.display = 'none';
        htmx.process(div);

        formScrollToElement('#shareholders')
    }


}