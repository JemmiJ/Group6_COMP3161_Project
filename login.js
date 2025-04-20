const loginform = document.getElementById('loginForm');
const alertdiv = document.getElementById('alert');

loginform.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    try {
        const response = await axios.post('http://127.0.0.1:8000/login', {
            username,
            password
        });

        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            alertdiv.innerHTML = '<div class ="alert alert-success">Login successful! Redirecting...</div>';
            setTimeout(() => {
                window.location.href ='dashboard.html';
            }, 1500);
        } else {
            alertdiv.innerHTML = '<div class="alert alert-danger">Incorrect Username or Password. Please try again.</div>';
        }
    } catch (error) {
        console.error(error);
        alertdiv.innerHTML = '<div class="alert alert-danger">Error logging in. Please try again later.</div>';
    }
});