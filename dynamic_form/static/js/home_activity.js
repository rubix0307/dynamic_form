function add_home_target_market() {
    var inputs = document.querySelectorAll('#home_company_activity_markets .home_company_activity_market');
    var hasEmpty = false;

    inputs.forEach(function(input) {
        if (input.value.trim() === '') {
            input.classList.remove('empty-input');
            input.classList.add('empty-input');
            setTimeout(function() {
                input.classList.remove('empty-input');
            }, 1000);
            hasEmpty = true;
        } else {
            input.classList.remove('empty-input');
        }
    });

    // Если есть пустые поля, не добавляем новое поле
    if (hasEmpty) {
        return;
    }


    var newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'home_company_activity_market';
    newInput.placeholder = 'Введите название целевого рынка';
    newInput.className = 'home_company_activity_market';

    document.getElementById('home_company_activity_markets').appendChild(newInput);
}