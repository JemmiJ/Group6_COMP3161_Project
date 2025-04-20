const signupform = document.getElementById('signupForm');
const alertdiv = document.getElementById('alert');

signupform.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const role = document.getElementById('role').value;

    if (!role) {
        alertdiv.innerHTML = '<div class="alert alert-warning">Please select a role.</div>';
        return;
    }

    try {
        const response = await axios.post('http://127.0.0.1:8000/signup', {
            username,
            password,
            role
        });

        if (response.data.success) {
            alertdiv.innerHTML = '<div class ="alert alert-success">Sign up successful! Redirecting to login...</div>';
            setTimeout(() => {
                window.location.href ='login.html';
            }, 1500);
        } else {
            alertdiv.innerHTML = '<div class="alert alert-danger">Sign up failed. Please try again.</div>';
        }
    } catch (error) {
        console.error(error);
        alertdiv.innerHTML = '<div class="alert alert-danger">Error signing up. Please try again later.</div>';
    }
});