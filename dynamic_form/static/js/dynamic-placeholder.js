document.addEventListener("DOMContentLoaded", function() {
    function createTypingAnimation(input) {
        var places = input.getAttribute('data-dynamic-placeholder').split(', ');
        var index = 0;
        var charIndex = 0;
        var currentText = '';
        var isDeleting = false;

        function typePlaceholder() {
            var currentPlace = places[index];

            if (isDeleting) {
                currentText = currentPlace.substring(0, charIndex--);
            } else {
                currentText = currentPlace.substring(0, charIndex++);
            }

            input.setAttribute('placeholder', currentText);

            if (!isDeleting && charIndex === currentPlace.length) {
                setTimeout(() => isDeleting = true, 1000); // Пауза перед удалением
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                index = (index + 1) % places.length;
            }

            var speed = isDeleting ? 50 : 100;
            setTimeout(typePlaceholder, speed);
        }

        typePlaceholder();
    }

    function initializeTypingAnimations() {
        document.querySelectorAll('[data-dynamic-placeholder]').forEach(createTypingAnimation);
    }

    // Инициализация для уже существующих элементов
    initializeTypingAnimations();

    // Наблюдатель для динамически добавленных элементов
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && node.hasAttribute('data-dynamic-placeholder')) {
                        createTypingAnimation(node);
                    }
                    if (node.nodeType === 1) {
                        node.querySelectorAll('[data-dynamic-placeholder]').forEach(createTypingAnimation);
                    }
                });
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
