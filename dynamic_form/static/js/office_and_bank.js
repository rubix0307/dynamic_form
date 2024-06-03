function listenBank() {
    const radioButtons = document.querySelectorAll('input[name="bank_account"]');
    const officeDetail = document.getElementById('office-detail');

    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.value === 'company' && this.checked) {
                officeDetail.innerHTML = '';

                const div = document.createElement('div');
                div.setAttribute('hx-post', 'get_form/?part=office');
                div.setAttribute('hx-trigger', 'load');
                div.setAttribute('hx-target', '#office-detail');
                div.setAttribute('hx-swap', 'innerHTML');

                document.body.appendChild(div);
                htmx.process(div);
            } else if ((this.value === 'no' || this.value === 'private') && this.checked) {
                officeDetail.innerHTML = '';
            }
        });
    });

}

function listenOffice() {
    const radioButtons = document.querySelectorAll('input[name="office"]');
    const officeArea = document.getElementById('real_office_area');

    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.value === 'real' && this.checked) {
                officeArea.style.display = 'block';
            } else {
                officeArea.style.display = 'none';
            }
        });
    });
}