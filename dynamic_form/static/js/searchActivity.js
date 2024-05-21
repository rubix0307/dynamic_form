function clearInput(element, selectors) {
    const parent = element.closest('.search');
    if (parent) {
        const input = parent.querySelector('input');
        if (input) {
            input.value = '';
            filterList('', selectors);
        }
    }
}
function listenSearchActivity() {
    document.getElementById('id_search_activity').addEventListener('input', function() {
        filterList(this.value.toLowerCase(), '#activity-suggestions ul');
    });
}


function filterList(filter, selectors) {
    var ul = document.querySelector(selectors);
    var li = ul.getElementsByTagName('li');

    for (var i = 0; i < li.length; i++) {
        var text = li[i].innerText.toLowerCase();
        if (filter && text.indexOf(filter) === -1) {
            li[i].classList.add('search-hidden');
        } else {
            li[i].classList.remove('search-hidden');
        }
    }
}