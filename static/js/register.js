document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const usernameMessage = document.getElementById('username-message');
    const emailMessage = document.getElementById('email-message');
    const errorMessage = document.getElementById('error-message');

    usernameInput.addEventListener('input', function() {
        const username = usernameInput.value;
        if (username) {
            checkUsernameAvailability(username);
        } else {
            usernameMessage.innerText = '';
            usernameMessage.classList.remove('tooltip-visible');
            usernameInput.classList.remove('error');
        }
    });

    emailInput.addEventListener('input', function() {
        const email = emailInput.value;
        if (email) {
            checkEmailAvailability(email);
        } else {
            emailMessage.innerText = '';
            emailMessage.classList.remove('tooltip-visible');
            emailInput.classList.remove('error');
        }
    });

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission

        const username = usernameInput.value;
        const email = emailInput.value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;

        // Perform validation checks
        if (password !== confirmPassword) {
            displayErrorMessage('Passwords do not match', errorMessage, document.getElementById('confirm-password-container'));
            return;
        }

        if (usernameMessage.innerText.includes('already taken')) {
            displayErrorMessage('Username is already taken', errorMessage, document.getElementById('username-container'));
            return;
        }

        if (emailMessage.innerText.includes('already taken')) {
            displayErrorMessage('Email is already taken', errorMessage, document.getElementById('email-container'));
            return;
        }

        // If all validations pass, submit the form
        this.submit();
    });

    function checkUsernameAvailability(username) {
        fetch('/check_username', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username })
        })
        .then(response => response.json())
        .then(data => {
            if (data.available) {
                showMessage(usernameMessage, 'Username is available', 'green', usernameInput);
            } else {
                showMessage(usernameMessage, 'Username is already taken', 'red', usernameInput);
            }
        })
        .catch(error => {
            console.error('Error checking username availability:', error);
            showMessage(usernameMessage, 'Error checking username availability', 'red', usernameInput);
        });
    }

    function checkEmailAvailability(email) {
        fetch('/check_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.available) {
                showMessage(emailMessage, 'Email is available', 'green', emailInput);
            } else {
                showMessage(emailMessage, 'Email is already taken', 'red', emailInput);
            }
        })
        .catch(error => {
            console.error('Error checking email availability:', error);
            showMessage(emailMessage, 'Error checking email availability', 'red', emailInput);
        });
    }

    function showMessage(element, message, color, input) {
        element.innerText = message;
        element.style.color = 'white';
        element.style.backgroundColor = color;
        positionTooltip(input, element);
        element.classList.add('tooltip-visible');
        if (color === 'red') {
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
    }

    function displayErrorMessage(message, element, container) {
        element.innerText = message;
        element.style.color = 'white';
        element.style.backgroundColor = 'red';
        positionTooltip(container.querySelector('input'), element);
        element.classList.add('tooltip-visible');
        container.classList.add('error');

        setTimeout(() => {
            element.classList.remove('tooltip-visible');
            container.classList.remove('error');
        }, 3000);
    }

    function positionTooltip(input, tooltip) {
        const rect = input.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
    
       
        tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
        tooltip.style.left = `${rect.left + window.scrollX}px`;
    
        
        const exceedsRight = rect.left + tooltipRect.width > window.innerWidth;
        if (exceedsRight) {
            
            tooltip.style.left = `${rect.right + window.scrollX - tooltipRect.width}px`;
        }
    }
});