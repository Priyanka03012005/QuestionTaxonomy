// // Wait for the DOM to fully load before running the script
// document.addEventListener('DOMContentLoaded', () => {
    
//     // Selecting the form elements
//     const usernameInput = document.getElementById('username');
//     const passwordInput = document.getElementById('password');
//     const loginButton = document.querySelector('button[type="submit"]');
    
//     // Event listener for login button
//     loginButton.addEventListener('click', (event) => {
//         event.preventDefault(); // Prevents form from submitting
//         handleLogin();
//     });

//     // Function to handle login
//     function handleLogin() {
//         const username = usernameInput.value;
//         const password = passwordInput.value;

//         // Basic form validation
//         if (username === '' || password === '') {
//             alert('Please fill in both username and password fields.');
//             return;
//         }

//         // if (!validateUsername(username)) {
//         //     alert('Please enter a valid username.');
//         //     return;
//         // }

//         // Simulate login process (for demonstration purposes)
//         alert(`Logging in with username: ${username}`);
//         // Here you would add logic to handle login (e.g., redirecting or API calls)
//     }

//     // Username validation function (assuming it's an email for now)
//     // function validateUsername(username) {
//     //     const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//     //     return re.test(username);
//     // }

//     // Optional: Forgot password link action
//     const forgotPasswordLink = document.querySelector('.forgot-password');
//     forgotPasswordLink.addEventListener('click', () => {
//         alert('Forgot Password functionality will be implemented.');
//     });
// });
