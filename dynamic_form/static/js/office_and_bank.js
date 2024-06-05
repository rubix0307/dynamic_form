function listenBank() {
    const radioButtons = document.querySelectorAll('input[name="bank_account"]');
    const officeDetail = document.getElementById('office-detail');
    const bankAccountDetail = document.getElementById('bank-account-detail');

    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.value === 'company' && this.checked) {
                officeDetail.innerHTML = '';
                bankAccountDetail.style.display = 'block';

                const div = document.createElement('div');
                div.setAttribute('hx-post', 'get_form/?part=office');
                div.setAttribute('hx-trigger', 'load');
                div.setAttribute('hx-target', '#office-detail');
                div.setAttribute('hx-swap', 'innerHTML');
                document.body.appendChild(div);
                htmx.process(div);


                const bankAccount = document.createElement('div');
                bankAccount.setAttribute('hx-post', 'get_form/?part=bank_account');
                bankAccount.setAttribute('hx-trigger', 'load');
                bankAccount.setAttribute('hx-target', '#bank-account-form');
                bankAccount.setAttribute('hx-swap', 'innerHTML');
                document.body.appendChild(bankAccount);
                htmx.process(bankAccount);



            } else if ((this.value === 'no' || this.value === 'private') && this.checked) {
                let bankAccountForm = document.getElementById('bank-account-form');
                officeDetail.innerHTML = '';
                bankAccountDetail.style.display = 'none';
                bankAccountForm.innerHTML = '';
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