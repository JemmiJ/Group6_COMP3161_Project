if (!localStorage.getItem('token')) {
    alert('Please login first.');
    window.location.href = 'login.html';
}

async function fetchCourses() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/courses', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        const coursediv = document.getElementById('courses');
        response.data.forEach(course => {
            const div = document.createElement('div');
            div.className = 'col-md-4';
            div.innerHTML = `
            <div class="dashboard-container">
                <div class = "course-header">
                    <h5>${course.courseName}</h5>
                    <button class="btn btn-primary btn-sm" onclick="enroll(${course.courseID})">Enroll</button>
                </div>
                <small>Code: ${course.courseCode}</small><br>
                <small>Department: ${course.department}</small>
            </div>
            `;
            coursediv.appendChild(div);
        });
    }
    catch (error) {
        console.error(error)
        alert('Failed to load courses.');
    }
}

async function enroll(courseId) {
    try {
        await axios.post(`http://127.0.0.1:8000/enroll/${courseId}`, {}, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        alert('Successfully enrolled');
    }
    catch (error) {
        console.error(error);
        alert('Enrollment failed');
    }
}

async function fetchAssignments() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/assignments', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        const assigndiv = document.getElementById('assignments');
        response.data.forEach(assign => {
            const div = document.createElement('div');
            div.className = 'col-md-6';
            div.innerHTML = `
                <div class="dashboard-container">
                    <h5>${assign.title}</h5>
                    <p>${assign.description}</p>
                    <small>Due: ${new Date(assign.dueDate).toLocaleDateString()}</small>
                </div>
            `;
            assigndiv.appendChild(div);
        });
    }
    catch (error) {
        console.error(error);
        alert('Failed to load assignments.');
    }
}

document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
});

fetchCourses();
fetchAssignments();