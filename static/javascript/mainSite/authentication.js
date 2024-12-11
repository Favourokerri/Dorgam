let password = document.getElementById('password');
let confirmPassword = document.getElementById('confirm-password');
let form = document.getElementById('signUpForm');

// Function to check password length and display error message
const checkPasswordLength = () => {
    let errorMessage = document.getElementById('password-form-error');
    if (password.value.length < 8) {
        errorMessage.style.display = "block";
        return true;
    } else {
        errorMessage.style.display = "none";
        return false;
    }
};

// Function to check if passwords match
const checkPasswordMatch = () => {
    let errorMessage = document.getElementById('ConfirmPassword-form-error');
    if (confirmPassword.value !== password.value) {
        errorMessage.style.display = "block";
        return true;
    } else {
        errorMessage.style.display = "none";
        return false;
    }
};

// Check length and match on input
password.addEventListener('input', () => {
    checkPasswordLength();
    checkPasswordMatch();
});

confirmPassword.addEventListener('input', () => {
    checkPasswordMatch();
});

// Handle form submission
form.addEventListener('submit', (e) => {
    let lengthError = checkPasswordLength();
    let matchError = checkPasswordMatch(); 
    if (lengthError || matchError) {
        e.preventDefault();
    }
});
