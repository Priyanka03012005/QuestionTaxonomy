// // Wait for the DOM to fully load before running the script
// document.addEventListener('DOMContentLoaded', () => {

//     // Selecting the form elements
//     const usernameInput = document.getElementById('username');
//     const passwordInput = document.getElementById('password');
//     const signupButton = document.querySelector('.signup-buttons button');

//     // Event listener for the Signup button
//     signupButton.addEventListener('click', (event) => {
//         event.preventDefault(); // Prevents form from submitting
//         handleSignup();
//     });

//     // Function to handle signup
//     function handleSignup() {
//         const username = usernameInput.value;
//         const password = passwordInput.value;
//         const role = document.getElementById('role').value; // Get the selected role from the dropdown

//         // Basic form validation
//         if (username === '' || password === '') {
//             alert('Please fill in both username and password fields.');
//             return;
//         }

//         if (!validateUsername(username)) {
//             alert('Please enter a valid username (only alphanumeric characters allowed).');
//             return;
//         }

//         // Simulate signup process (for demonstration purposes)
//         if (role === 'admin') {
//             alert(`Signing up as Admin with username: ${username}`);
//             // Add your logic to handle admin signup (e.g., API call)
//         } else if (role === 'user') {
//             alert(`Signing up as User with username: ${username}`);
//             // Add your logic to handle user signup
//         }
//     }

//     // Username validation function (checks for alphanumeric characters)
//     // function validateUsername(username) {
//     //     const re = /^[a-zA-Z0-9_]+$/; // Alphanumeric pattern with underscore allowed
//     //     return re.test(username);
//     // }

//     // // Optional: Login link action
//     // const loginLink = document.querySelector('.login-option a');
//     // loginLink.addEventListener('click', (event) => {
//     //     event.preventDefault();
//     //     alert('Login functionality will be implemented.');
//     // });
// });
