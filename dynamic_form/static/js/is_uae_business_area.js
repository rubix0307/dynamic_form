function listenUAEBusinessArea() {
    const radioButtons = document.querySelectorAll('input[name="uae_business_area"]');
    const businessAreaDetail = document.getElementById('uae-business-area-detail');

    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.value === '1' && this.checked) {
                businessAreaDetail.style.display = 'block';

                const div = document.createElement('div');
                div.setAttribute('hx-post', 'get_form/?part=uae_business_area_detail');
                div.setAttribute('hx-trigger', 'load');
                div.setAttribute('hx-target', '#uae-business-area-detail');
                div.setAttribute('hx-swap', 'innerHTML');

                document.body.appendChild(div);
                htmx.process(div);
            } else if (this.value === '0' && this.checked) {
                businessAreaDetail.innerHTML = '';
            }
        });
    });

}

function UAEBusinessAreaCheck(btn) {
    let is_good = true
    let radioAnswered = checkRadioGroups('data-UAEBusinessArea-check-radio');

    if (!radioAnswered) {
        is_good = false;
    }

    if (is_good) {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=activities');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#activities');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        btn.style.display = 'none';
        htmx.process(div);

        formScrollToElement('#activities')
    }

}