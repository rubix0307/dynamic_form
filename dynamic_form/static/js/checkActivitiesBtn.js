function observeActivities() {
    // Найти элемент, за которым нужно следить, и кнопку
    let targetNode = document.getElementById('selected-activities');
    let checkActivitiesBtn = document.getElementById('checkActivitiesBtn');

    // Настройки наблюдателя (какие изменения отслеживать)
    let config = {
      childList: true, // отслеживать добавление или удаление дочерних элементов
    };

    // Callback-функция при возникновении мутаций
    let callback = function(mutationsList, observer) {
      for (let mutation of mutationsList) {
        if (mutation.type === 'childList') {
          // Проверить, пустой ли элемент
          if (targetNode.children.length > 0) {
            checkActivitiesBtn.style.display = 'block';

          } else {
            checkActivitiesBtn.style.display = 'none';
          }
        }
      }
    };

    // Создать экземпляр наблюдателя, связав его с callback-функцией
    let observer = new MutationObserver(callback);

    // Начать наблюдение за элементом с указанными настройками
    observer.observe(targetNode, config);

    // Проверить начальное состояние элемента (на случай, если он уже не пустой)
    if (targetNode.children.length > 0) {
      checkActivitiesBtn.style.display = 'block';
    } else {
      checkActivitiesBtn.style.display = 'none';
    }
}
observeActivities()
function highlightEmptyActivityPlaces() {
    // Найти все элементы с классом activity-place внутри selected-activities
    const activityPlaces = document.querySelectorAll('#selected-activities .activity-place');

    // Итерироваться по найденным activity-place
    let allGood = true
    activityPlaces.forEach(activityPlace => {
        // Найти все input с типом checkbox внутри текущего activity-place
        const checkboxes = activityPlace.querySelectorAll('input[type="checkbox"]');

        // Проверить, есть ли хотя бы один отмеченный чекбокс
        const hasCheckedCheckbox = Array.from(checkboxes).some(checkbox => checkbox.checked);

        // Если нет ни одного отмеченного чекбокса, выделить activity-place красным
        if (!hasCheckedCheckbox) {
            activityPlace.style.border = '2px solid var(--tg-theme-accent-text-color)';
            allGood = false
        } else {
            // Убрать красное выделение, если есть отмеченные чекбоксы
            activityPlace.style.border = '';
        }
    });

    if (allGood) {
        const elementsToHide = document.querySelectorAll('[data-hidecheckingactivities="1"]');
        elementsToHide.forEach(element => {
            element.style.display = 'none';
        });
        const elementsToNotActive = document.querySelectorAll('[data-notactivecheckingactivities="1"]');
        elementsToNotActive.forEach(element => {
            element.style.pointerEvents = 'none';
        });
    }
}