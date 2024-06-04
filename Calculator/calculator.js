document.addEventListener('DOMContentLoaded', function() {
    let currentInput = '';
    let operator = null;
    let firstOperand = null;
    let secondOperand = null;

    const inputElement = document.querySelector('input');
    const operatorSymbols = {
        plus: '+',
        minus: '-',
        multiply: '*',
        divide: '/'
    };
    const numberButtons = Array.from(document.querySelectorAll('[data-number]'));
    numberButtons.forEach(button => {
        button.addEventListener('click', function() {
            currentInput += this.dataset.number;
            inputElement.value = currentInput;
        });
    });

    const clearButton = document.querySelector('[data-clear]');
    clearButton.addEventListener('click', function() {
        firstOperand = null;
        operator = null;
        currentInput = '';
        inputElement.value = '';
    });

    const operatorButtons = Array.from(document.querySelectorAll('[data-operator]'));
    operatorButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (!firstOperand) {
                firstOperand = currentInput;
                operator = this.dataset.operator;
                currentInput = '';
                inputElement.value = firstOperand + ' ' + operatorSymbols[operator];
            } else if (firstOperand && !currentInput) {
                operator = this.dataset.operator;
                inputElement.value = firstOperand + ' ' + operatorSymbols[operator];
            }
        });
    });

    const equalsButton = document.querySelector('[data-equals]');
    equalsButton.addEventListener('click', function() {
        if (firstOperand && operator) {
            secondOperand = currentInput;
            switch (operator) {
                case 'plus':
                    inputElement.value = parseFloat(firstOperand) + parseFloat(secondOperand);
                    break;
                case 'minus':
                    inputElement.value = parseFloat(firstOperand) - parseFloat(secondOperand);
                    break;
                case 'multiply':
                    inputElement.value = parseFloat(firstOperand) * parseFloat(secondOperand);
                    break;
                case 'divide':
                    inputElement.value = parseFloat(firstOperand) / parseFloat(secondOperand);
                    break;
            }
            firstOperand = null;
            operator = null;
            currentInput = '';
        }
    });
});