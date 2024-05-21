function removeActivity(button) {
    var activityPlace = button.closest('.secondary-place');
    activityPlace.remove();
    var dataUrl = activityPlace.getAttribute('data-url');
    var liElements = document.querySelectorAll('#activity-suggestions li');
    liElements.forEach(function(li) {
        if (li.getAttribute('hx-get') === dataUrl) {
            li.style.display = '';
        }
    });
}