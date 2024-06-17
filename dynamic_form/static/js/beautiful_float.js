document.addEventListener('DOMContentLoaded', () => {
    function adjustFontSizeForDataPrice() {
        const adjustFontSizeForDecimal = (element) => {
            const value = element.getAttribute('data-price');
            const numberParts = value.split('.');
            let formattedNumber = numberParts[0]; // Integral part

            if (numberParts.length > 1) {
                const decimalPart = numberParts[1]; // Decimal part
                formattedNumber += '.<span class="decimal">' + decimalPart + '</span>';
            }

            element.innerHTML = formattedNumber;
        };

        const elements = document.querySelectorAll('[data-price]');
        elements.forEach(element => adjustFontSizeForDecimal(element));

        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1 && node.hasAttribute('data-price')) {
                            adjustFontSizeForDecimal(node);
                        }
                        node.querySelectorAll?.('[data-price]').forEach(childNode => {
                            adjustFontSizeForDecimal(childNode);
                        });
                    });
                }
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    // Initial call
    adjustFontSizeForDataPrice();
});
