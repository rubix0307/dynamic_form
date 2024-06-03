
function addLegalCounselShareholder(elementId, shareholderNumber) {
    const place = document.getElementById(elementId);
    const placeList = place.querySelector('.list');
    const inputElement = document.createElement('input');
    inputElement.type = 'text';
    inputElement.id = `shareholder_${shareholderNumber}_jurisdictions`;
    inputElement.name = inputElement.id;
    inputElement.placeholder = 'Введите юрисдикцию';
    inputElement.setAttribute('data-block7-input-value-required', '1')
    placeList.appendChild(inputElement);
}


function listenShareholderLegalCount() {
    const shareholderCountInput = document.getElementById('shareholder-legal-count');
    const shareholderDetailDiv = document.getElementById('shareholder-legal-detail');

    shareholderCountInput.addEventListener('input', () => {
        const count = parseInt(shareholderCountInput.value, 10) || 0;
        const currentCount = shareholderDetailDiv.querySelectorAll('.place').length;
        const questionDiv = shareholderDetailDiv.querySelector('.question');

        if (count === 0) {
            shareholderDetailDiv.style.display = 'none';
        } else {
            shareholderDetailDiv.style.display = 'block';
        }


        if (count > currentCount) {
            for (let i = currentCount + 1; i <= count; i++) {
                const placeDiv = document.createElement('div');
                placeDiv.className = 'place';
                placeDiv.id = `shareholder_${i}_jurisdictions_list`;


                placeDiv.innerHTML = `
                <div class="caption">Акционер ${i}</div>
                <div class="list"></div>
                <div class="add" onclick="addLegalCounselShareholder('${placeDiv.id}', ${i})">
                <div class="symbol">+</div>Добавить еще</div>
                `;
                shareholderDetailDiv.appendChild(placeDiv);
                addLegalCounselShareholder(placeDiv.id, i)
            }
        } else if (count < currentCount) {
            for (let i = currentCount; i > count; i--) {
                shareholderDetailDiv.removeChild(shareholderDetailDiv.lastChild);
            }
        }
    });
}

function updateShareholderList() {
    const privateShareholderCountInput = document.getElementById('private-shareholder-count');
    const shareholderLegalCountInput = document.getElementById('shareholder-legal-count');
    const shareholdersNationalityList = document.getElementById('shareholders-nationality-list');

    const privateShareholderCount = parseInt(privateShareholderCountInput.value, 10);
    const shareholderLegalCount = parseInt(shareholderLegalCountInput.value, 10);

    const totalShareholders = privateShareholderCount + shareholderLegalCount;
    if ((privateShareholderCount >= 0 && shareholderLegalCount >= 0)) {
        shareholdersNationalityList.style.display = 'block';

        // Clear existing blocks if needed
        while (shareholdersNationalityList.querySelectorAll('.nationality').length > totalShareholders) {
            shareholdersNationalityList.removeChild(shareholdersNationalityList.lastChild);
        }

        // Add new blocks if needed
        while (shareholdersNationalityList.querySelectorAll('.nationality').length < totalShareholders) {
            let t = shareholdersNationalityList.querySelectorAll('.nationality').length + 1


            shareholdersNationalityList.appendChild(createShareholderBlock(t));
            addNationalityInput(t)
        }
    } else {
        shareholdersNationalityList.style.display = 'none';
    }

    if (totalShareholders === 0) {
        shareholdersNationalityList.style.display = 'none';
    }
}
function addNationalityInput(i) {
    const container = document.getElementById(`shareholder-${i}-nationality-list`);
    if (!container) {
        console.error(`Container with id "shareholder-${i}-nationality-list" not found.`);
        return;
    }

    const input = document.createElement('input');
    input.type = 'text';
    input.id = `shareholder_${i}_nationality_input`;
    input.name = `shareholder_${i}_nationality_input`;
    input.placeholder = 'Введите гражданство';
    input.dataset.block7InputValueRequired = '1';

    const listContainer = container.querySelector('.list');
    if (!listContainer) {
        console.error('List container not found within shareholder block.');
        return;
    }

    listContainer.appendChild(input);
}

function createShareholderBlock(i) {
    const container = document.createElement('div');
    container.id = `shareholder-${i}-nationality-list`;
    container.className = `nationality`;

    container.innerHTML = `

        <div class="caption">Акционер ${i}</div>
        <div class="list"></div>

        <div class="add" onclick="addNationalityInput(${i})"><div class="symbol">+</div>Добавить еще</div> 
    `;
    return container;
}

function listenAllShareholdersCount(){
    const privateShareholderCountInput = document.getElementById('private-shareholder-count');
    const shareholderLegalCountInput = document.getElementById('shareholder-legal-count');

    privateShareholderCountInput.addEventListener('input', updateShareholderList);
    shareholderLegalCountInput.addEventListener('input', updateShareholderList);
}
function checkInputsBlock7(btn) {
    let is_good = true;
    let allInputsWithValue = checkInputValueExists('data-block7-input-value-required');



    if (!allInputsWithValue) {
        is_good = false;
    }

    if (is_good) {
        const div = document.createElement('div');
        div.setAttribute('hx-post', 'get_form/?part=customer_data');
        div.setAttribute('hx-trigger', 'load');
        div.setAttribute('hx-target', '#customer_data');
        div.setAttribute('hx-swap', 'innerHTML');

        document.body.appendChild(div);
        btn.style.display = 'none';
        htmx.process(div);

        formScrollToElement('#customer_data')
    }




}




